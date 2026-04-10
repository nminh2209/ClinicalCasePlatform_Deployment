#!/usr/bin/env python3
"""
Extraction + heading-matching accuracy diagnostic.

Runs the full OCR pipeline on a given image/PDF, then prints:
  1. Per-stage timing (detection / merge / crop / recognition / autofill)
  2. Raw OCR text (line by line, numbered)
  3. Line-length histogram (to spot suspicious short crops / bad detection)
  4. Headings extracted by the regex layer
  5. SBERT match for every extracted heading — including below-threshold ones
     (so we can see which are "almost matched" and candidates for new synonyms)
  6. FIELD_MAPPINGS coverage: which template fields never got any close match
  7. Final autofill structured output

Usage (inside the backend container):
    docker exec -it clinical_backend bash -lc \\
        "cd /app && python ai/ocr/test_extraction_accuracy.py \\
         ai/ocr/data/benhantonghop_page-01.png"

Optional flags:
    --threshold 0.5   Lower confidence threshold (default 0.6)
    --show-text       Print the full OCR text block
    --show-all-matches  Print match for ALL extracted headings (default: only rejected)
"""

import argparse
import os
import sys
import time
from collections import Counter
from statistics import mean, median

# Set up Django before importing anything that touches the ORM/models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_backend.settings")
# Suppress HuggingFace Hub chatter for clean benchmark output
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging  # noqa: E402

for noisy in ("httpx", "urllib3", "huggingface_hub", "sentence_transformers"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

import django  # noqa: E402

django.setup()

from ai.ocr.ocr_service import ocr_service  # noqa: E402
from ai.ocr import heading_matcher as hm  # noqa: E402
from ai.ocr.heading_matcher import (  # noqa: E402
    HeadingMatcher,
    FIELD_MAPPINGS,
    extract_headings_from_text,
    autofill_from_ocr,
)


def banner(title: str):
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def fmt_pct(x: float) -> str:
    return f"{x * 100:5.1f}%"


def line_histogram(lines):
    """Bucket lines by character count to spot bad-crop patterns."""
    if not lines:
        return
    buckets = Counter()
    for line in lines:
        n = len(line)
        if n == 0:
            buckets["empty"] += 1
        elif n < 5:
            buckets["1-4 chars"] += 1
        elif n < 15:
            buckets["5-14 chars"] += 1
        elif n < 40:
            buckets["15-39 chars"] += 1
        elif n < 80:
            buckets["40-79 chars"] += 1
        else:
            buckets["80+ chars"] += 1

    order = ["empty", "1-4 chars", "5-14 chars", "15-39 chars", "40-79 chars", "80+ chars"]
    lengths = [len(l) for l in lines]
    print(f"  total lines      : {len(lines)}")
    print(f"  total characters : {sum(lengths)}")
    print(f"  mean length      : {mean(lengths):.1f}")
    print(f"  median length    : {median(lengths):.1f}")
    print(f"  max length       : {max(lengths)}")
    print("  length distribution:")
    for key in order:
        if buckets[key]:
            bar = "#" * min(40, buckets[key])
            print(f"    {key:<12} {buckets[key]:4d} {bar}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Path to an image or PDF (relative to /app)")
    parser.add_argument(
        "--threshold", type=float, default=0.6, help="SBERT confidence threshold"
    )
    parser.add_argument(
        "--show-text", action="store_true", help="Print the full raw OCR text"
    )
    parser.add_argument(
        "--show-all-matches",
        action="store_true",
        help="Print match results for every extracted heading, not only rejected ones",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(2)

    banner(f"1. OCR EXTRACTION — {args.file}")
    t0 = time.time()
    ocr_result = ocr_service.process(args.file)
    extract_elapsed = time.time() - t0

    text = ocr_result.get("text", "")
    lines = [l for l in text.split("\n") if l.strip()]
    pages = ocr_result.get("pages", [])
    metadata = ocr_result.get("metadata", {})

    print(f"  engine           : {metadata.get('engine')}")
    print(f"  total time       : {extract_elapsed:.2f}s")
    print(f"  pages            : {metadata.get('page_count')}")
    print(f"  elapsed_ms (lib) : {metadata.get('elapsed_ms')}")

    banner("2. LINE-LENGTH DISTRIBUTION")
    line_histogram(lines)

    # Count region types across all pages for extraction diagnostics
    region_counts = Counter()
    for page in pages:
        for region in page.get("regions", []):
            region_counts[region.get("type", "unknown")] += 1
    if region_counts:
        print("\n  regions detected :")
        for t, n in region_counts.most_common():
            print(f"    {t:<12} {n}")

    if args.show_text:
        banner("3. RAW OCR TEXT")
        for i, line in enumerate(lines, 1):
            print(f"  {i:4d}: {line}")

    banner("4. HEADING EXTRACTION (regex layer)")
    heading_pairs = extract_headings_from_text(text)
    print(f"  headings extracted: {len(heading_pairs)}")
    for i, (h, c) in enumerate(heading_pairs, 1):
        preview = c.replace("\n", " \u23ce ")[:70]
        print(f"  {i:3d}. {h!r:<35} -> {preview!r}")

    if not heading_pairs:
        print("\n  [!] NO headings were extracted from the OCR text.")
        print("      This means the regex layer is the bottleneck, not SBERT.")
        print("      Inspect the raw text with --show-text to see what the")
        print("      document actually looks like and tune the patterns.")
        sys.exit(0)

    banner("5. SBERT MATCHING DIAGNOSTIC")
    # Use threshold 0.0 for the diagnostic so we see ALL matches, even
    # below the rejection line — this is how we discover near-misses. We
    # prime the module-level singleton used by `autofill_from_ocr` here so
    # section 7 can reuse the same embeddings without reloading SBERT.
    hm._matcher_instance = HeadingMatcher(confidence_threshold=0.0)
    diag_matcher = hm._matcher_instance
    headings_only = [h for h, _ in heading_pairs]
    matches = diag_matcher.match_all_headings(headings_only)

    matched = []
    borderline = []  # score in [threshold-0.15, threshold)
    rejected = []
    for h in headings_only:
        field, score = matches[h]
        # match_all_headings with threshold=0.0 never returns (None, score);
        # we apply the real threshold manually here.
        if score >= args.threshold:
            matched.append((h, field, score))
        elif score >= args.threshold - 0.15:
            borderline.append((h, field, score))
        else:
            rejected.append((h, field, score))

    print(f"  threshold        : {args.threshold}")
    print(f"  matched (>=thr)  : {len(matched)}")
    print(f"  borderline       : {len(borderline)}  (within 0.15 below threshold)")
    print(f"  rejected         : {len(rejected)}")

    print("\n  MATCHED:")
    for h, field, score in matched:
        print(f"    {fmt_pct(score)}  {h!r:<35} -> {field}")

    if borderline:
        print("\n  BORDERLINE (likely candidates for new FIELD_MAPPINGS synonyms):")
        for h, field, score in borderline:
            print(f"    {fmt_pct(score)}  {h!r:<35} -> would-be: {field}")

    if rejected and args.show_all_matches:
        print("\n  REJECTED (not a template field, or very poor match):")
        for h, field, score in rejected:
            print(f"    {fmt_pct(score)}  {h!r:<35} -> nearest: {field}")
    elif rejected:
        print(f"\n  REJECTED: {len(rejected)} headings (pass --show-all-matches to see)")

    banner("6. FIELD_MAPPINGS COVERAGE")
    # Which template fields received no match on this page?
    matched_fields = {field for _, field, _ in matched}
    all_fields = set(FIELD_MAPPINGS.keys())
    unmatched_fields = all_fields - matched_fields
    print(f"  template fields  : {len(all_fields)}")
    print(f"  matched on page  : {len(matched_fields)}")
    print(f"  coverage         : {fmt_pct(len(matched_fields) / len(all_fields))}")
    if matched_fields:
        print("\n  matched fields:")
        for field in sorted(matched_fields):
            print(f"    + {field}")

    banner("7. FINAL AUTOFILL OUTPUT")
    # Section 5 primed the module singleton with threshold=0.0 so we could
    # inspect near-misses. For the final autofill we must restore the real
    # threshold before calling autofill_from_ocr — otherwise rejected hits
    # like "EPA 1" at 35% would leak into the structured output.
    if hm._matcher_instance is not None:
        hm._matcher_instance.confidence_threshold = args.threshold
    t_af = time.time()
    structured = autofill_from_ocr(text, args.threshold)
    af_elapsed = time.time() - t_af
    print(f"  autofill time    : {af_elapsed:.2f}s")
    print(f"  top-level keys   : {len(structured)}")
    for key, value in structured.items():
        if isinstance(value, dict) and "value" in value:
            preview = value["value"].replace("\n", " \u23ce ")[:70]
            print(f"    {key:<40} = {preview!r}  ({value['confidence']:.2f})")
        elif isinstance(value, dict):
            print(f"    {key}:")
            for child_key, child_val in value.items():
                if isinstance(child_val, dict) and "value" in child_val:
                    preview = child_val["value"].replace("\n", " \u23ce ")[:60]
                    print(
                        f"      {child_key:<36} = {preview!r}  "
                        f"({child_val['confidence']:.2f})"
                    )

    banner("SUMMARY")
    print(f"  Extraction time       : {extract_elapsed:.2f}s")
    print(f"  Autofill time         : {af_elapsed:.2f}s")
    print(f"  Headings extracted    : {len(heading_pairs)}")
    print(f"  Headings matched      : {len(matched)} / {len(heading_pairs)}")
    print(
        f"  Heading match rate    : "
        f"{fmt_pct(len(matched) / len(heading_pairs)) if heading_pairs else 'n/a'}"
    )
    print(f"  Unique fields filled  : {len(matched_fields)}")
    print()


if __name__ == "__main__":
    main()
