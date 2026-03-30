"""
Seed default case choice tables (priority/complexity).
Usage: python manage.py seed_case_choices
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from cases.specialty_models import CasePriorityLevel, CaseComplexityLevel


class Command(BaseCommand):
    help = "Seed default case priority and complexity levels"

    def handle(self, *args, **options):
        priority_rows = [
            {"name": "Thấp", "key": "low", "color": "green", "display_order": 1},
            {"name": "Trung bình", "key": "medium", "color": "yellow", "display_order": 2},
            {"name": "Cao", "key": "high", "color": "orange", "display_order": 3},
            {"name": "Khẩn cấp", "key": "urgent", "color": "red", "display_order": 4},
        ]

        complexity_rows = [
            {
                "name": "Cơ bản",
                "key": "basic",
                "description": "Trường hợp đơn giản, phù hợp nhập môn",
                "display_order": 1,
            },
            {
                "name": "Trung bình",
                "key": "intermediate",
                "description": "Trường hợp mức độ trung bình",
                "display_order": 2,
            },
            {
                "name": "Nâng cao",
                "key": "advanced",
                "description": "Trường hợp phức tạp hơn, cần phân tích sâu",
                "display_order": 3,
            },
            {
                "name": "Chuyên gia",
                "key": "expert",
                "description": "Trường hợp rất phức tạp",
                "display_order": 4,
            },
        ]

        created_priority = 0
        updated_priority = 0
        priority_errors = 0
        
        for i, row in enumerate(priority_rows):
            try:
                _, created = CasePriorityLevel.objects.update_or_create(
                    key=row["key"],
                    defaults={
                        "name": row["name"],
                        "color": row["color"],
                        "display_order": row["display_order"],
                        "is_active": True,
                    },
                )
                if created:
                    created_priority += 1
                else:
                    updated_priority += 1
            except (ValidationError, IntegrityError, TypeError, KeyError) as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error seeding priority level {i+1} ({row.get('key', 'unknown')}): {e}"
                    )
                )
                priority_errors += 1

        created_complexity = 0
        updated_complexity = 0
        complexity_errors = 0
        
        for i, row in enumerate(complexity_rows):
            try:
                _, created = CaseComplexityLevel.objects.update_or_create(
                    key=row["key"],
                    defaults={
                        "name": row["name"],
                        "description": row["description"],
                        "display_order": row["display_order"],
                        "is_active": True,
                    },
                )
                if created:
                    created_complexity += 1
                else:
                    updated_complexity += 1
            except (ValidationError, IntegrityError, TypeError, KeyError) as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error seeding complexity level {i+1} ({row.get('key', 'unknown')}): {e}"
                    )
                )
                complexity_errors += 1

        # Final report
        if priority_errors == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Priority levels: created={created_priority}, updated={updated_priority}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Priority levels: created={created_priority}, updated={updated_priority}, errors={priority_errors}"
                )
            )
        
        if complexity_errors == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Complexity levels: created={created_complexity}, updated={updated_complexity}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Complexity levels: created={created_complexity}, updated={updated_complexity}, errors={complexity_errors}"
                )
            )
        
        if priority_errors > 0 or complexity_errors > 0:
            raise CommandError(
                f"Seeding failed with {priority_errors + complexity_errors} error(s). "
                "Check model fields match seed data keys."
            )

        self.stdout.write(
            self.style.SUCCESS("\nSeed operation completed successfully!")
        )
