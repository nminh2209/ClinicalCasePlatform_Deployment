"""
Management command to reset and repopulate test data
"""

from django.core.management.base import BaseCommand
from cases.models import (
    Case,
    ClinicalHistory,
    PhysicalExamination,
    Investigations,
    DiagnosisManagement,
    LearningOutcomes,
    StudentNotes,
    CasePermission,
)
from comments.models import Comment
from feedback.models import Feedback
from grades.models import Grade


class Command(BaseCommand):
    help = "Reset database and populate with fresh test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-confirm",
            action="store_true",
            help="Skip confirmation prompt",
        )

    def handle(self, *args, **options):
        if not options["skip_confirm"]:
            confirm = input(
                "This will DELETE ALL data except users and repositories. Continue? (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return

        self.stdout.write(
            self.style.WARNING("Deleting all case-related data and templates...")
        )

        # Delete in reverse order of dependencies
        StudentNotes.objects.all().delete()
        CasePermission.objects.all().delete()
        Comment.objects.all().delete()
        Feedback.objects.all().delete()
        Grade.objects.all().delete()

        # Delete medical sections
        ClinicalHistory.objects.all().delete()
        PhysicalExamination.objects.all().delete()
        Investigations.objects.all().delete()
        DiagnosisManagement.objects.all().delete()
        LearningOutcomes.objects.all().delete()

        # Delete cases
        Case.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS("Data and templates deleted successfully!")
        )

        # Repopulate with test data by running the script
        self.stdout.write(self.style.WARNING("Populating fresh test data..."))

        import subprocess
        import os
        import sys

        # Get the path to populate_test_data.py (in backend directory)
        backend_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        script_path = os.path.join(backend_dir, "populate_test_data.py")

        if os.path.exists(script_path):
            try:
                # Run the populate script using the same Python interpreter
                result = subprocess.run(
                    [sys.executable, script_path],
                    cwd=backend_dir,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    self.stdout.write(
                        self.style.SUCCESS("Test data populated successfully!")
                    )
                    if result.stdout:
                        self.stdout.write(result.stdout)
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Error populating test data: {result.stderr}")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to run populate script: {str(e)}")
                )
        else:
            self.stdout.write(
                self.style.WARNING(f"populate_test_data.py not found at {script_path}")
            )

        self.stdout.write(self.style.SUCCESS("Database reset complete!"))
