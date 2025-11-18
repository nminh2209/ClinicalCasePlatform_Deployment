from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .medical_models import MedicalTerm, ICD10Code, MedicalAbbreviation


class TerminologyTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email="admin@example.com", username="admin", password="pass"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        MedicalTerm.objects.create(
            term="Viêm phổi",
            vietnamese_term="Viêm phổi",
            english_term="Pneumonia",
            synonyms=["pneumonia"],
        )
        MedicalTerm.objects.create(
            term="Sốt xuất huyết",
            vietnamese_term="Sốt xuất huyết",
            english_term="Dengue fever",
            synonyms=["dengue"],
        )
        ICD10Code.objects.create(
            code="J18",
            description_en="Pneumonia unspecified",
            description_vi="Viêm phổi không rõ tác nhân",
        )
        MedicalAbbreviation.objects.create(abbr="BP", expansion="Blood Pressure")

    def test_autocomplete_simple(self):
        url = reverse("terminology-terms-autocomplete")
        resp = self.client.get(url, {"q": "Viêm"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(
            any(
                "Viêm phổi" in (t.get("vietnamese_term") or t.get("term")) for t in data
            )
        )

    def test_icd_search(self):
        url = reverse("terminology-icd10")
        resp = self.client.get(url, {"q": "Pneumonia"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any(d["code"] == "J18" for d in data))

    def test_abbreviation_lookup(self):
        url = reverse("terminology-abbreviations")
        resp = self.client.get(url, {"q": "BP"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any(d["abbr"] == "BP" for d in data))
