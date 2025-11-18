#!/usr/bin/env python
"""
Test the case detail view directly to debug the 500 error
"""

import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from cases.views import CaseDetailView
from cases.models import Case
import traceback

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinical_case_platform.settings_test")
django.setup()

User = get_user_model()


def test_case_detail_view():
    print("🔍 Testing Case Detail View Directly")
    print("=" * 50)

    try:
        # Get the ICU case
        case = Case.objects.get(id=9)
        print(f"✅ Found case: {case.title}")

        # Get a user
        user = User.objects.get(email="student@test.com")
        print(f"✅ Found user: {user.email}")

        # Create a request
        factory = RequestFactory()
        request = factory.get(f"/api/cases/{case.id}/")
        request.user = user

        # Test the view
        view = CaseDetailView()
        view.setup(request, pk=case.id)

        # Get the object
        print("🔍 Testing get_object()...")
        obj = view.get_object()
        print(f"✅ get_object() successful: {obj.title}")

        # Get the serializer
        print("🔍 Testing get_serializer()...")
        serializer_class = view.get_serializer_class()
        print(f"✅ Serializer class: {serializer_class.__name__}")

        # Test serialization
        print("🔍 Testing serialization...")
        serializer = serializer_class(obj)
        data = serializer.data
        print("✅ Serialization successful")

        # Check sections
        sections = [
            "clinical_history",
            "physical_examination",
            "detailed_investigations",
            "diagnosis_management",
            "learning_outcomes",
        ]
        print("\n🏥 Available sections:")
        for section in sections:
            if section in data and data[section]:
                print(f"   ✅ {section}: Available")
            else:
                print(f"   ❌ {section}: Missing")

        print("\n🎉 SUCCESS: View is working correctly!")

    except Exception as e:
        print(f"❌ ERROR in view: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()


if __name__ == "__main__":
    test_case_detail_view()
