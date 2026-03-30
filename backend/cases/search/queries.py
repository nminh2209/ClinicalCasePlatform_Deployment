import unicodedata
from typing import List
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Cast
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from cases.models import Case
from cases.search.utils import build_search_text


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


def rank_cases(
    base_qs: models.QuerySet,
    query: str,
):
    fts_query_text = build_search_text(query)
    if not fts_query_text:
        return base_qs.none()

    trigram_query = unaccent(fts_query_text)

    search_query = SearchQuery(
        fts_query_text,
        config="vietnamese",
        search_type="plain",
    )

    return (
        base_qs.annotate(
            fts_rank=SearchRank(
                F("search_document"),
                search_query,
            ),
            trigram_score=TrigramSimilarity(
                "search_text",
                trigram_query,
            ),
        )
        .filter(Q(search_document=search_query) | Q(trigram_score__gt=0.005))
        .annotate(score=(F("fts_rank") * Value(0.7) + F("trigram_score") * Value(0.3)))
        .order_by("-score")
    )
