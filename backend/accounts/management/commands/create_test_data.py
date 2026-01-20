from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import User
from cases.models import Case
from repositories.models import Repository


class Command(BaseCommand):
    help = "Create test data for development and testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing test data before creating new data",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("🧪 Creating test data for Clinical Case Platform...")
        )

        try:
            with transaction.atomic():
                if options["reset"]:
                    self.stdout.write("🗑️ Resetting test data...")
                    # Delete test data (be careful not to delete production data)
                    Case.objects.filter(title__icontains="Sample").delete()
                    Repository.objects.filter(name__icontains="Test").delete()
                    User.objects.filter(email__endswith="@test.com").delete()

                # Create test users
                self.stdout.write("👥 Creating test users...")

                # Student user
                student1, created = User.objects.get_or_create(
                    email="student1@test.com",
                    defaults={
                        "username": "student1@test.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": User.RoleChoices.STUDENT,
                    },
                )
                if created:
                    student1.set_password("testpass123")
                    student1.save()
                    self.stdout.write(f"  ✅ Created student: {student1.email}")
                else:
                    self.stdout.write(f"  ℹ️ Student exists: {student1.email}")

                # Instructor user
                instructor1, created = User.objects.get_or_create(
                    email="instructor1@test.com",
                    defaults={
                        "username": "instructor1@test.com",
                        "first_name": "Dr. Jane",
                        "last_name": "Smith",
                        "role": User.RoleChoices.INSTRUCTOR,
                    },
                )
                if created:
                    instructor1.set_password("testpass123")
                    instructor1.save()
                    self.stdout.write(f"  ✅ Created instructor: {instructor1.email}")
                else:
                    self.stdout.write(f"  ℹ️ Instructor exists: {instructor1.email}")

                # Second student
                student2, created = User.objects.get_or_create(
                    email="student2@test.com",
                    defaults={
                        "username": "student2@test.com",
                        "first_name": "Sarah",
                        "last_name": "Johnson",
                        "role": User.RoleChoices.STUDENT,
                    },
                )
                if created:
                    student2.set_password("testpass123")
                    student2.save()
                    self.stdout.write(f"  ✅ Created student: {student2.email}")
                else:
                    self.stdout.write(f"  ℹ️ Student exists: {student2.email}")

                # Create test repositories
                self.stdout.write("📁 Creating test repositories...")

                repo1, created = Repository.objects.get_or_create(
                    name="Test Repository - Cardiology",
                    defaults={
                        "owner": student1,
                        "description": "Test repository for cardiology cases",
                        "is_public": True,
                    },
                )
                if created:
                    self.stdout.write(f"  ✅ Created repository: {repo1.name}")

                repo2, created = Repository.objects.get_or_create(
                    name="Test Repository - General Medicine",
                    defaults={
                        "owner": instructor1,
                        "description": "Test repository for general medicine cases",
                        "is_public": True,
                    },
                )
                if created:
                    self.stdout.write(f"  ✅ Created repository: {repo2.name}")

                # Create sample cases
                self.stdout.write("📋 Creating sample cases...")

                case1, created = Case.objects.get_or_create(
                    title="Sample Cardiology Case - Acute MI",
                    defaults={
                        "student": student1,
                        "repository": repo1,
                        "patient_name": "Patient Alpha (anonymized)",
                        "patient_age": 58,
                        "patient_gender": "male",
                        "specialty": "Cardiology",
                        "history": "A 58-year-old male presents with acute onset severe chest pain radiating to left arm. Pain started 2 hours ago while at rest. Associated with sweating and nausea. Past medical history significant for hypertension and diabetes.",
                        "examination": "Patient appears distressed. Vital signs: BP 160/95, HR 110, RR 22, O2 sat 96%. Cardiovascular examination reveals regular rhythm, no murmurs. Chest clear to auscultation.",
                        "investigations": "ECG shows ST elevation in leads II, III, aVF. Troponin I elevated at 15.2 ng/mL. Chest X-ray normal.",
                        "diagnosis": "ST-elevation myocardial infarction (STEMI) - inferior wall",
                        "treatment": "Primary PCI performed. Dual antiplatelet therapy initiated. ACE inhibitor and beta-blocker started. Patient education on lifestyle modifications.",
                        "keywords": "cardiology, STEMI, myocardial infarction, chest pain",
                        "case_status": Case.StatusChoices.SUBMITTED,
                        "learning_objectives": "Understanding STEMI presentation, ECG interpretation, emergency management of acute MI",
                    },
                )
                if created:
                    self.stdout.write(f"  ✅ Created case: {case1.title}")

                case2, created = Case.objects.get_or_create(
                    title="Sample Internal Medicine Case - Diabetes",
                    defaults={
                        "student": student2,
                        "repository": repo2,
                        "patient_name": "Patient Beta (anonymized)",
                        "patient_age": 45,
                        "patient_gender": "female",
                        "specialty": "Internal Medicine",
                        "history": "A 45-year-old female presents with polyuria, polydipsia, and weight loss over 3 months. Family history of diabetes mellitus type 2.",
                        "examination": "BMI 28. Vital signs stable. Fundoscopy shows early diabetic retinopathy. No other significant findings.",
                        "diagnosis": "Diabetes mellitus type 2, newly diagnosed",
                        "treatment": "Metformin initiated. Dietary counseling provided. HbA1c monitoring planned. Referral to diabetes educator.",
                        "keywords": "diabetes, internal medicine, polyuria, polydipsia",
                        "case_status": Case.StatusChoices.DRAFT,
                        "learning_objectives": "Understanding diabetes presentation, diagnostic criteria, initial management",
                    },
                )
                if created:
                    self.stdout.write(f"  ✅ Created case: {case2.title}")

                case3, created = Case.objects.get_or_create(
                    title="Sample Emergency Case - Acute Asthma",
                    defaults={
                        "student": student1,
                        "repository": repo1,
                        "patient_name": "Patient Gamma (anonymized)",
                        "patient_age": 28,
                        "patient_gender": "female",
                        "specialty": "Emergency Medicine",
                        "history": "A 28-year-old female with known asthma presents with acute shortness of breath and wheeze. Symptoms started after exposure to cat dander.",
                        "examination": "Patient in moderate distress. Widespread wheeze on auscultation. Peak flow 40% of predicted. Accessory muscle use noted.",
                        "diagnosis": "Acute asthma exacerbation",
                        "treatment": "Nebulized salbutamol and ipratropium. Oral prednisolone. Observation and monitoring. Discharge with action plan.",
                        "keywords": "asthma, emergency, wheeze, bronchospasm",
                        "case_status": Case.StatusChoices.REVIEWED,
                        "learning_objectives": "Acute asthma management, severity assessment, discharge planning",
                    },
                )
                if created:
                    self.stdout.write(f"  ✅ Created case: {case3.title}")

                self.stdout.write(
                    self.style.SUCCESS(
                        "\n🎉 Test data creation completed successfully!"
                    )
                )
                self.stdout.write("\n📊 Summary:")
                self.stdout.write(f"  Users: {User.objects.count()}")
                self.stdout.write(f"  Repositories: {Repository.objects.count()}")
                self.stdout.write(f"  Cases: {Case.objects.count()}")

                self.stdout.write("\n🔐 Test Login Credentials:")
                self.stdout.write("  Admin: admin@test.com / testpass123")
                self.stdout.write("  Student 1: student1@test.com / testpass123")
                self.stdout.write("  Student 2: student2@test.com / testpass123")
                self.stdout.write("  Instructor: instructor1@test.com / testpass123")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating test data: {str(e)}")
            )
            raise
