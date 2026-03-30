from django.db import models

from django.contrib.postgres.search import SearchVector
from django.db import transaction
import unicodedata

from cases.models import Case
from cases.models import CaseSearchToken


from cases.search.utils import build_search_text

from django.db.models.signals import post_save, post_delete
from django.db.models import F
from django.dispatch import receiver

from cases.medical_models import ClinicalHistory
from cases.medical_models import LearningOutcomes
from cases.medical_models import PhysicalExamination
from cases.medical_models import Investigations
from cases.medical_models import DiagnosisManagement


@receiver(post_save, sender=Case)
def case_post_save(sender, instance, update_fields=None, **kwargs):
    if update_fields and {"search_document", "search_text"} <= set(update_fields):
        return
    update_case_search(instance)


@receiver(post_save, sender=ClinicalHistory)
@receiver(post_delete, sender=ClinicalHistory)
def clinical_history_changed(sender, instance, **kwargs):
    update_case_search(instance.case)


@receiver(post_save, sender=LearningOutcomes)
@receiver(post_delete, sender=LearningOutcomes)
def learning_outcomes_changed(sender, instance, **kwargs):
    update_case_search(instance.case)


@receiver(post_save, sender=PhysicalExamination)
@receiver(post_delete, sender=PhysicalExamination)
def physical_examination_changed(sender, instance, **kwargs):
    update_case_search(instance.case)


@receiver(post_save, sender=Investigations)
@receiver(post_delete, sender=Investigations)
def investigations_changed(sender, instance, **kwargs):
    update_case_search(instance.case)


@receiver(post_save, sender=DiagnosisManagement)
@receiver(post_delete, sender=DiagnosisManagement)
def diagnosis_management_changed(sender, instance, **kwargs):
    update_case_search(instance.case)


def unaccent(text: str) -> str:
    """
    Normalize text for pg_trgm:
    - Remove Vietnamese diacritics
    - Lowercase
    """
    if not text:
        return ""

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()



@transaction.atomic
def update_case_search(case: Case):
    """
    Rebuild search_document and search_text for a Case.

    """

    # --- Collect related data (mirrors your LEFT JOINs) ---

    ch = getattr(case, "clinical_history", None)
    pe = getattr(case, "physical_examination", None)
    inv = getattr(case, "investigations_detail", None)
    dm = getattr(case, "diagnosis_management", None)
    lo = getattr(case, "learning_outcomes", None)

    # --- Build weighted text  ---

    text_A = build_search_text(
        case.title,
        case.case_summary,
        case.chief_complaint_brief,
        getattr(dm, "primary_diagnosis", None),
        getattr(dm, "differential_diagnosis", None),
    )

    text_B = build_search_text(
        case.keywords,
        case.learning_tags,
        getattr(ch, "chief_complaint", None),
        getattr(ch, "history_present_illness", None),
        getattr(dm, "treatment_plan", None),
        getattr(dm, "prognosis", None),
        getattr(lo, "learning_objectives", None),
        getattr(lo, "key_concepts", None),
    )

    text_C = build_search_text(
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


    # --- Raw text for trigram (same as your unaccent pipeline later) ---
    case.search_text = unaccent(f"{text_A} {text_B} {text_C}")

    # --- Weighted SearchVector ---
    case.search_document = (
        SearchVector(models.Value(text_A), weight="A", config="vietnamese")
        + SearchVector(models.Value(text_B), weight="B", config="vietnamese")
        + SearchVector(models.Value(text_C), weight="C", config="vietnamese")
    )

    case.save(update_fields=["search_document", "search_text"])
