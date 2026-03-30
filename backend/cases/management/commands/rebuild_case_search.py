from django.core.management.base import BaseCommand
from django.db import transaction
from collections import Counter

from cases.models import Case
from cases.search.signals import update_case_search
from cases.models import CaseSearchToken
from cases.search.utils import build_full_segmented_text,unaccent
from collections import defaultdict


class Command(BaseCommand):
    help = "Rebuild PostgreSQL FTS search_document and search_text for all cases"

    def handle(self, *args, **options):
        total = Case.objects.count()
        self.stdout.write(f"Rebuilding search index for {total} cases...")

        # Step 1 — Clear token table
        CaseSearchToken.objects.all().delete()

        token_counter = defaultdict(lambda: {"display": "", "freq": 0})

        for idx, case in enumerate(
            Case.objects.select_related(
                "clinical_history",
                "physical_examination",
                "investigations_detail",
                "diagnosis_management",
                "learning_outcomes",
            ).iterator(),
            start=1,
        ):  #Rebuild FTS fields
            update_case_search(case)
            # Collect tokens from segmented text
            
            segmented_text = build_full_segmented_text(case)
            original_tokens = set(segmented_text.split())

            for original in original_tokens:
                if not original:
                    continue

                # Display form (restore spacing for UI)
                display = original.replace("_", " ")

                # Normalized search key (no accent, lowercase)
                normalized = unaccent(original)

                entry = token_counter[normalized]
                entry["display"] = display
                entry["freq"] += 1

            if idx % 50 == 0:
                self.stdout.write(f"Processed {idx}/{total}")

        # Step 2 — Bulk insert tokens
        token_objects = [
            CaseSearchToken(
                token=normalized,
                display=data["display"],
                frequency=data["freq"],
            )
            for normalized, data in token_counter.items()
        ]
        CaseSearchToken.objects.bulk_create(token_objects)

        self.stdout.write(self.style.SUCCESS("Search index rebuild complete"))