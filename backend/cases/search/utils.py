import logging
import unicodedata
import re
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def normalize_text(text: Optional[str]) -> str:
    """
    Normalize Vietnamese text for search:
    - Unicode normalization
    - Lowercasing
    - Whitespace cleanup
    """
    if not text:
        return ""

    # Normalize unicode
    text = unicodedata.normalize("NFC", text)

    # Lowercase
    text = text.lower()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

def unaccent(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()


try:
    import py_vncorenlp
except ImportError:
    py_vncorenlp = None


_VNCORENLP = None
_VNCORENLP_UNAVAILABLE = False  # set to True after a failed init attempt


def get_vncorenlp():
    """
    Lazy singleton for VnCoreNLP word segmentation.
    Returns None if Java or py_vncorenlp is unavailable.
    """
    global _VNCORENLP, _VNCORENLP_UNAVAILABLE

    if _VNCORENLP_UNAVAILABLE:
        return None

    if _VNCORENLP is None:
        if py_vncorenlp is None:
            _VNCORENLP_UNAVAILABLE = True
            logger.warning("py_vncorenlp is not installed; falling back to plain tokenization.")
            return None
        try:
            current_dir = Path(__file__).resolve().parent
            save_dir = str(current_dir)
            _VNCORENLP = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=save_dir)
        except Exception as exc:
            _VNCORENLP_UNAVAILABLE = True
            logger.warning(
                "VnCoreNLP unavailable (likely missing JAVA_HOME): %s. "
                "Falling back to plain tokenization.",
                exc,
            )
            return None

    return _VNCORENLP


def segment_text(text: str) -> str:
    """
    Segment Vietnamese text using VnCoreNLP word_segment,
    then merge multi-word tokens so PostgreSQL FTS
    treats them as a single lexeme.
    Falls back to plain whitespace tokenization when VnCoreNLP/Java is unavailable.
    """
    if not text:
        return ""

    vncorenlp = get_vncorenlp()

    if vncorenlp is None:
        # Fallback: return normalized text unchanged (already whitespace-clean)
        return text

    # word_segment returns list[str]
    segmented_sentences = vncorenlp.word_segment(text)

    tokens = []
    for sentence in segmented_sentences:
        for token in sentence.split():
            # Merge multi-word tokens: Đại_học -> ĐạiHọc
            if "_" in token:
                token = token.replace("_", "")
            tokens.append(token)

    return " ".join(tokens)


def segment_text_normal(text: str) -> str:
    """
    Segment Vietnamese text using VnCoreNLP word_segment.
    Falls back to plain whitespace tokenization when VnCoreNLP/Java is unavailable.
    """
    if not text:
        return ""

    vncorenlp = get_vncorenlp()

    if vncorenlp is None:
        return text

    # word_segment returns list[str]
    segmented_sentences = vncorenlp.word_segment(text)

    tokens = []
    for sentence in segmented_sentences:
        for token in sentence.split():
            tokens.append(token)

    return " ".join(tokens)



def build_search_text(*parts: Optional[str]) -> str:
    """
    Combine multiple text fields into a single
    normalized + segmented search string.
    """
    combined = " ".join(p for p in parts if p)

    normalized = normalize_text(combined)
    segmented = segment_text(normalized)

    return segmented


def build_search_text_normal(*parts: Optional[str]) -> str:
    """
    Combine multiple text fields into a single
    normalized + segmented search string.
    """
    combined = " ".join(p for p in parts if p)

    normalized = normalize_text(combined)
    segmented = segment_text_normal(normalized)

    return segmented



def build_full_segmented_text(case):
    ch = getattr(case, "clinical_history", None)
    pe = getattr(case, "physical_examination", None)
    inv = getattr(case, "investigations_detail", None)
    dm = getattr(case, "diagnosis_management", None)
    lo = getattr(case, "learning_outcomes", None)

    text_A = build_search_text_normal(
        case.title,
        case.case_summary,
        case.chief_complaint_brief,
        getattr(dm, "primary_diagnosis", None),
        getattr(dm, "differential_diagnosis", None),
    )

    text_B = build_search_text_normal(
        case.keywords,
        case.learning_tags,
        getattr(ch, "chief_complaint", None),
        getattr(ch, "history_present_illness", None),
        getattr(dm, "treatment_plan", None),
        getattr(dm, "prognosis", None),
        getattr(lo, "learning_objectives", None),
        getattr(lo, "key_concepts", None),
    )

    text_C = build_search_text_normal(
        getattr(ch, "past_medical_history", None),
        getattr(ch, "family_history", None),
        getattr(ch, "social_history", None),
        getattr(ch, "review_systems", None),
        getattr(ch, "allergies", None),
        getattr(ch, "medications", None),
        getattr(pe, "general_appearance", None),
        getattr(pe, "vital_signs", None),
        getattr(pe, "cardiovascular", None),
        getattr(pe, "respiratory", None),
        getattr(pe, "abdominal", None),
        getattr(pe, "neurological", None),
        getattr(pe, "musculoskeletal", None),
        getattr(pe, "skin", None),
        getattr(inv, "laboratory_results", None),
        getattr(inv, "imaging_studies", None),
        getattr(inv, "ecg_findings", None),
        getattr(inv, "pathology_results", None),
        getattr(inv, "microbiology_results", None),
        getattr(lo, "clinical_pearls", None),
        getattr(lo, "discussion_points", None),
    )

    return f"{text_A} {text_B} {text_C}"