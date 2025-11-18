"""
Management command to validate cases
Usage: python manage.py validate_cases --all
"""

from django.core.management.base import BaseCommand
from django.db.models import Q

from cases.models import Case
from cases.validation import (
    CaseValidationRule,
    CaseValidationResult,
    CaseQualityMetrics,
)


class Command(BaseCommand):
    help = "Validate cases against defined rules"

    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", help="Validate all cases")
        parser.add_argument("--case-id", type=int, help="Validate specific case by ID")
        parser.add_argument(
            "--status",
            type=str,
            choices=["draft", "submitted", "reviewed", "approved"],
            help="Validate cases with specific status",
        )
        parser.add_argument(
            "--recalculate-quality",
            action="store_true",
            help="Recalculate quality metrics for all cases",
        )

    def handle(self, *args, **options):
        if options["recalculate_quality"]:
            self.recalculate_quality_metrics()
            return

        # Determine which cases to validate
        if options["case_id"]:
            cases = Case.objects.filter(id=options["case_id"])
        elif options["status"]:
            cases = Case.objects.filter(case_status=options["status"])
        elif options["all"]:
            cases = Case.objects.all()
        else:
            self.stdout.write(
                self.style.ERROR("Please specify --all, --case-id, or --status")
            )
            return

        if not cases.exists():
            self.stdout.write(self.style.WARNING("No cases found to validate"))
            return

        self.stdout.write(f"Validating {cases.count()} cases...")

        validated_count = 0
        passed_count = 0
        failed_count = 0
        warning_count = 0

        for case in cases:
            result = self.validate_case(case)
            validated_count += 1

            if result.validation_status == "passed":
                passed_count += 1
            elif result.validation_status == "failed":
                failed_count += 1
            elif result.validation_status == "warning":
                warning_count += 1

            if validated_count % 10 == 0:
                self.stdout.write(f"  Validated {validated_count} cases...")

        self.stdout.write(self.style.SUCCESS(f"\nValidation completed!"))
        self.stdout.write(f"  Total: {validated_count}")
        self.stdout.write(self.style.SUCCESS(f"  Passed: {passed_count}"))
        self.stdout.write(self.style.WARNING(f"  Warnings: {warning_count}"))
        self.stdout.write(self.style.ERROR(f"  Failed: {failed_count}"))

    def validate_case(self, case):
        """Validate a single case"""
        # Get applicable rules
        rules = CaseValidationRule.objects.filter(is_active=True)

        # Filter by template
        if case.template:
            rules = rules.filter(
                Q(applies_to_templates__isnull=True)
                | Q(applies_to_templates=case.template)
            )

        # Filter by specialty
        rules = rules.filter(
            Q(applies_to_specialties=[])
            | Q(applies_to_specialties__contains=[case.specialty])
        )

        # Validate against each rule
        validation_issues = []
        rules_passed = 0
        rules_failed = 0
        warnings_count = 0

        for rule in rules:
            is_valid, error_message = rule.validate_case(case)

            if not is_valid:
                issue = {
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "field": rule.target_field,
                    "message": error_message,
                    "help_text": rule.help_text,
                }
                validation_issues.append(issue)

                if rule.severity == "error":
                    rules_failed += 1
                elif rule.severity == "warning":
                    warnings_count += 1
            else:
                rules_passed += 1

        # Determine overall status
        if rules_failed > 0:
            validation_status = "failed"
        elif warnings_count > 0:
            validation_status = "warning"
        else:
            validation_status = "passed"

        # Calculate quality metrics
        quality_metrics, created = CaseQualityMetrics.objects.get_or_create(case=case)
        quality_metrics.calculate_completeness()

        # Calculate scores
        total_rules = rules.count()
        completeness_score = (
            (rules_passed / total_rules * 100) if total_rules > 0 else 0
        )
        quality_score = quality_metrics.overall_quality
        overall_score = completeness_score * 0.6 + quality_score * 0.4

        # Create or update validation result
        validation_result = CaseValidationResult.objects.create(
            case=case,
            validation_status=validation_status,
            total_rules_checked=total_rules,
            rules_passed=rules_passed,
            rules_failed=rules_failed,
            warnings_count=warnings_count,
            validation_issues=validation_issues,
            completeness_score=completeness_score,
            quality_score=quality_score,
            overall_score=overall_score,
            validation_type="automatic",
        )

        return validation_result

    def recalculate_quality_metrics(self):
        """Recalculate quality metrics for all cases"""
        self.stdout.write("Recalculating quality metrics for all cases...")

        cases = Case.objects.all()
        updated_count = 0

        for case in cases:
            quality_metrics, created = CaseQualityMetrics.objects.get_or_create(
                case=case
            )
            quality_metrics.calculate_completeness()
            updated_count += 1

            if updated_count % 10 == 0:
                self.stdout.write(f"  Updated {updated_count} cases...")

        self.stdout.write(
            self.style.SUCCESS(
                f"Quality metrics recalculated for {updated_count} cases"
            )
        )
