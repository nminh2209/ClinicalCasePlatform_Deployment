# cases/apps.py

from django.apps import AppConfig


class CasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # type: ignore[attr-defined]
    name = "cases"
