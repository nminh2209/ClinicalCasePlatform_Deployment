"""
Management command to reset and repopulate test data
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from cases.models import (
    Case, ClinicalHistory, PhysicalExamination, 
    Investigations, DiagnosisManagement, LearningOutcomes,
    MedicalAttachment, StudentNotes, CasePermission
)
from comments.models import Comment
from feedback.models import Feedback
from grades.models import Grade


class Command(BaseCommand):
    help = 'Reset database and populate with fresh test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-confirm',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        if not options['skip_confirm']:
            confirm = input('This will DELETE ALL data except users, repositories, and templates. Continue? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        self.stdout.write(self.style.WARNING('Deleting all case-related data...'))

        # Delete in reverse order of dependencies
        StudentNotes.objects.all().delete()
        MedicalAttachment.objects.all().delete()
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

        self.stdout.write(self.style.SUCCESS('Data deleted successfully!'))

        # Repopulate with test data
        self.stdout.write(self.style.WARNING('Populating fresh test data...'))
        call_command('populate_test_data')

        self.stdout.write(self.style.SUCCESS('Database reset complete!'))
