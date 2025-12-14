"""
Comprehensive tests for the enhanced case sharing permissions system

Tests cover:
- Model functionality and validation
- Permission-based access control
- Time-limited sharing
- Department and class-based sharing
- Guest access system
- Bulk operations
- Audit logging
- API endpoints
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import secrets

from .models import Case, CasePermission, GuestAccess, CaseGroup, PermissionAuditLog
from .medical_models import Department
from repositories.models import Repository

User = get_user_model()


class CasePermissionModelTests(TestCase):
    """Test case permission model functionality"""

    def setUp(self):
        # Create test data
        self.department = Department.objects.create(
            name="Cardiology", code="CARD", vietnamese_name="Khoa Tim mạch"
        )

        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
            first_name="Dr. Jane",
            last_name="Smith",
            department=self.department,
        )

        self.student1 = User.objects.create_user(  # type: ignore[attr-defined]
            username="student1@test.com",
            email="student1@test.com",
            password="testpass123",
            role="student",
            first_name="John",
            last_name="Doe",
            department=self.department,
        )

        self.student2 = User.objects.create_user(  # type: ignore[attr-defined]
            username="student2@test.com",
            email="student2@test.com",
            password="testpass123",
            role="student",
            first_name="Alice",
            last_name="Johnson",
        )

        # Create repository and case
        self.repository = Repository.objects.create(
            name="Test Repository", description="Test repo", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="Test Case - Myocardial Infarction",
            student=self.student1,
            repository=self.repository,
            patient_name="Test Patient",
            patient_age=55,
            patient_gender="male",
            specialty="Cardiology",
        )

    def test_individual_permission_creation(self):
        """Test creating individual user permission"""
        permission = CasePermission.objects.create(
            case=self.case,
            user=self.student2,
            permission_type=CasePermission.PermissionChoices.VIEW,
            granted_by=self.instructor,
            share_type=CasePermission.ShareTypeChoices.INDIVIDUAL,
        )

        self.assertEqual(permission.case, self.case)
        self.assertEqual(permission.user, self.student2)
        self.assertEqual(permission.permission_type, "view")
        self.assertFalse(permission.is_expired)
        self.assertTrue(permission.is_active)

    def test_department_permission_creation(self):
        """Test creating department-wide permission"""
        permission = CasePermission.objects.create(
            case=self.case,
            target_department=self.department,
            permission_type=CasePermission.PermissionChoices.COMMENT,
            granted_by=self.instructor,
            share_type=CasePermission.ShareTypeChoices.DEPARTMENT,
        )

        self.assertEqual(permission.target_department, self.department)
        self.assertIsNone(permission.user)
        self.assertEqual(permission.share_type, "department")

    def test_class_group_permission_creation(self):
        """Test creating class group permission"""
        permission = CasePermission.objects.create(
            case=self.case,
            class_group="K15Y6",
            permission_type=CasePermission.PermissionChoices.ANALYZE,
            granted_by=self.instructor,
            share_type=CasePermission.ShareTypeChoices.CLASS_GROUP,
        )

        self.assertEqual(permission.class_group, "K15Y6")
        self.assertEqual(permission.permission_type, "analyze")

    def test_time_limited_permission(self):
        """Test time-limited permission expiration"""
        # Create permission that expires in 1 hour
        expires_at = timezone.now() + timedelta(hours=1)
        permission = CasePermission.objects.create(
            case=self.case,
            user=self.student2,
            permission_type=CasePermission.PermissionChoices.VIEW,
            granted_by=self.instructor,
            expires_at=expires_at,
        )

        self.assertFalse(permission.is_expired)

        # Mock time to be after expiration
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = expires_at + timedelta(minutes=1)
            self.assertTrue(permission.is_expired)

    def test_access_tracking(self):
        """Test permission access tracking"""
        permission = CasePermission.objects.create(
            case=self.case,
            user=self.student2,
            permission_type=CasePermission.PermissionChoices.VIEW,
            granted_by=self.instructor,
        )

        # Initial state
        self.assertEqual(permission.access_count, 0)
        self.assertIsNone(permission.last_accessed)

        # Update access
        permission.update_access()
        permission.refresh_from_db()

        self.assertEqual(permission.access_count, 1)
        self.assertIsNotNone(permission.last_accessed)


class GuestAccessModelTests(TestCase):
    """Test guest access model functionality"""

    def setUp(self):
        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
        )

        self.repository = Repository.objects.create(
            name="Test Repository", description="Test repo", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="Test Case",
            student=self.instructor,  # Using instructor as case creator
            repository=self.repository,
            patient_name="Test Patient",
            patient_age=45,
            patient_gender="female",
            specialty="Internal Medicine",
        )

    def test_guest_access_creation(self):
        """Test creating guest access"""
        expires_at = timezone.now() + timedelta(days=3)

        guest_access = GuestAccess.objects.create(
            case=self.case,
            access_token=secrets.token_urlsafe(32),
            guest_email="reviewer@external.com",
            guest_name="Dr. External Reviewer",
            permission_type=CasePermission.PermissionChoices.VIEW,
            created_by=self.instructor,
            expires_at=expires_at,
        )

        self.assertEqual(guest_access.case, self.case)
        self.assertEqual(guest_access.guest_email, "reviewer@external.com")
        self.assertFalse(guest_access.is_expired)
        self.assertEqual(guest_access.access_count, 0)
        self.assertEqual(len(guest_access.accessed_ips), 0)

    def test_guest_access_tracking(self):
        """Test guest access tracking"""
        guest_access = GuestAccess.objects.create(
            case=self.case,
            access_token=secrets.token_urlsafe(32),
            guest_email="reviewer@external.com",
            permission_type="view",
            created_by=self.instructor,
            expires_at=timezone.now() + timedelta(days=1),
        )

        # Track access with IP
        guest_access.update_access("192.168.1.100")
        guest_access.refresh_from_db()

        self.assertEqual(guest_access.access_count, 1)
        self.assertIn("192.168.1.100", guest_access.accessed_ips)
        self.assertIsNotNone(guest_access.last_accessed)

        # Track access from same IP (should not duplicate)
        guest_access.update_access("192.168.1.100")
        guest_access.refresh_from_db()

        self.assertEqual(guest_access.access_count, 2)
        self.assertEqual(guest_access.accessed_ips.count("192.168.1.100"), 1)


class CaseGroupModelTests(TestCase):
    """Test case group model functionality"""

    def setUp(self):
        self.department = Department.objects.create(name="Surgery", code="SURG")

        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
            department=self.department,
        )

        self.repository = Repository.objects.create(
            name="Surgery Repository",
            description="Surgery cases",
            owner=self.instructor,
        )

        # Create multiple cases
        self.case1 = Case.objects.create(
            title="Appendectomy Case",
            student=self.instructor,
            repository=self.repository,
            patient_name="Patient 1",
            patient_age=30,
            patient_gender="male",
            specialty="Surgery",
        )

        self.case2 = Case.objects.create(
            title="Cholecystectomy Case",
            student=self.instructor,
            repository=self.repository,
            patient_name="Patient 2",
            patient_age=45,
            patient_gender="female",
            specialty="Surgery",
        )

        self.students = []
        for i in range(3):
            student = User.objects.create_user(  # type: ignore[attr-defined]
                username=f"student{i}@test.com",
                email=f"student{i}@test.com",
                password="testpass123",
                role="student",
            )
            self.students.append(student)

    def test_case_group_creation(self):
        """Test creating case group"""
        case_group = CaseGroup.objects.create(
            name="Surgery Assignment Week 5",
            description="Basic surgical procedures",
            group_type=CaseGroup.GroupTypeChoices.ASSIGNMENT,
            created_by=self.instructor,
            department=self.department,
            class_identifier="K15Y5",
        )

        # Add cases to group
        case_group.cases.add(self.case1, self.case2)

        self.assertEqual(case_group.cases.count(), 2)
        self.assertEqual(case_group.group_type, "assignment")
        self.assertEqual(case_group.department, self.department)

    def test_bulk_permission_grant(self):
        """Test bulk permission granting via case group"""
        case_group = CaseGroup.objects.create(
            name="Surgery Assignment",
            created_by=self.instructor,
            class_identifier="K15Y5",
        )

        case_group.cases.add(self.case1, self.case2)

        # Grant permissions to all students for all cases in group
        created_count = case_group.add_bulk_permissions(
            users=self.students, permission_type="view"
        )

        # Should create 6 permissions (3 students × 2 cases)
        self.assertEqual(created_count, 6)

        # Verify permissions exist
        for student in self.students:
            self.assertTrue(
                CasePermission.objects.filter(
                    case=self.case1, user=student, permission_type="view"
                ).exists()
            )
            self.assertTrue(
                CasePermission.objects.filter(
                    case=self.case2, user=student, permission_type="view"
                ).exists()
            )


class PermissionAuditLogTests(TestCase):
    """Test permission audit logging"""

    def setUp(self):
        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
        )

        self.student = User.objects.create_user(  # type: ignore[attr-defined]
            username="student@test.com",
            email="student@test.com",
            password="testpass123",
            role="student",
        )

        self.repository = Repository.objects.create(
            name="Test Repository", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="Test Case",
            student=self.instructor,
            repository=self.repository,
            patient_name="Test Patient",
            patient_age=40,
            patient_gender="male",
            specialty="General",
        )

    def test_audit_log_creation(self):
        """Test creating audit log entries"""
        PermissionAuditLog.log_permission_change(
            case=self.case,
            target_user=self.student,
            actor_user=self.instructor,
            action=PermissionAuditLog.ActionChoices.GRANTED,
            permission_type="view",
            description="Granted view permission for assignment",
            additional_data={"assignment_id": "WEEK5"},
        )

        # Verify log entry
        log_entry = PermissionAuditLog.objects.first()
        self.assertEqual(log_entry.case, self.case)  # type: ignore[attr-defined]
        self.assertEqual(log_entry.target_user, self.student)  # type: ignore[attr-defined]
        self.assertEqual(log_entry.actor_user, self.instructor)  # type: ignore[attr-defined]
        self.assertEqual(log_entry.action, "granted")  # type: ignore[attr-defined]
        self.assertEqual(log_entry.additional_data["assignment_id"], "WEEK5")  # type: ignore[attr-defined]


class CasePermissionAPITests(APITestCase):
    """Test case permission API endpoints"""

    def setUp(self):
        # Create test users
        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
            first_name="Dr.",
            last_name="Smith",
        )

        self.student1 = User.objects.create_user(  # type: ignore[attr-defined]
            username="student1@test.com",
            email="student1@test.com",
            password="testpass123",
            role="student",
            first_name="John",
            last_name="Doe",
        )

        self.student2 = User.objects.create_user(  # type: ignore[attr-defined]
            username="student2@test.com",
            email="student2@test.com",
            password="testpass123",
            role="student",
            first_name="Alice",
            last_name="Johnson",
        )

        # Create case
        self.repository = Repository.objects.create(
            name="Test Repository", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="API Test Case",
            student=self.student1,
            repository=self.repository,
            patient_name="API Test Patient",
            patient_age=35,
            patient_gender="male",
            specialty="Cardiology",
        )

    def test_create_individual_permission(self):
        """Test creating individual permission via API"""
        self.client.force_authenticate(user=self.instructor)

        data = {
            "user": self.student2.id,
            "permission_type": "view",
            "share_type": "individual",
            "notes": "Assignment access",
        }

        response = self.client.post(
            f"/api/cases/{self.case.id}/permissions/",  # type: ignore[attr-defined]
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["permission_type"], "view")
        self.assertEqual(response.data["user"], self.student2.id)

        # Verify permission created
        permission = CasePermission.objects.get(case=self.case, user=self.student2)
        self.assertEqual(permission.granted_by, self.instructor)

    def test_bulk_grant_permissions(self):
        """Test bulk granting permissions"""
        self.client.force_authenticate(user=self.instructor)

        data = {
            "share_type": "individual",
            "users_ids": [self.student1.id, self.student2.id],
            "permission_type": "comment",
            "expires_hours": 48,
            "notes": "Peer review session",
        }

        response = self.client.post(
            f"/api/cases/{self.case.id}/permissions/bulk-grant/",  # type: ignore[attr-defined]
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["created_count"], 1
        )  # Only student2 since student1 owns the case

        # Verify permission created for student2
        permission = CasePermission.objects.get(case=self.case, user=self.student2)
        self.assertEqual(permission.permission_type, "comment")
        self.assertIsNotNone(permission.expires_at)

    def test_permission_access_denied(self):
        """Test access denied for unauthorized users"""
        self.client.force_authenticate(user=self.student2)

        response = self.client.get(f"/api/cases/{self.case.id}/permissions/")  # type: ignore[attr-defined]

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_permissions_as_owner(self):
        """Test listing permissions as case owner"""
        # Create a permission
        CasePermission.objects.create(
            case=self.case,
            user=self.student2,
            permission_type="view",
            granted_by=self.instructor,
        )

        self.client.force_authenticate(user=self.student1)  # Case owner

        response = self.client.get(f"/api/cases/{self.case.id}/permissions/")  # type: ignore[attr-defined]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class GuestAccessAPITests(APITestCase):
    """Test guest access API endpoints"""

    def setUp(self):
        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
        )

        self.repository = Repository.objects.create(
            name="Test Repository", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="Guest Access Test Case",
            student=self.instructor,
            repository=self.repository,
            patient_name="Test Patient",
            patient_age=50,
            patient_gender="female",
            specialty="Neurology",
        )

    def test_create_guest_access(self):
        """Test creating guest access"""
        self.client.force_authenticate(user=self.instructor)

        data = {
            "guest_email": "external@reviewer.com",
            "guest_name": "Dr. External",
            "permission_type": "view",
            "expiration_hours": 72,
        }

        response = self.client.post(
            f"/api/cases/{self.case.id}/guest-access/",  # type: ignore[attr-defined]
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["guest_email"], "external@reviewer.com")
        self.assertIn("access_token", response.data)

        # Verify guest access created
        guest_access = GuestAccess.objects.get(guest_email="external@reviewer.com")
        self.assertEqual(guest_access.case, self.case)
        self.assertEqual(guest_access.created_by, self.instructor)

    def test_guest_access_via_token(self):
        """Test accessing case via guest token"""
        # Create guest access
        guest_access = GuestAccess.objects.create(
            case=self.case,
            access_token="test_token_123",
            guest_email="guest@test.com",
            permission_type="view",
            created_by=self.instructor,
            expires_at=timezone.now() + timedelta(days=1),
        )

        # Access case without authentication
        response = self.client.get("/api/guest-access/test_token_123/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("case", response.data)
        self.assertIn("guest_access", response.data)

        # Verify access was tracked
        guest_access.refresh_from_db()
        self.assertEqual(guest_access.access_count, 1)

    def test_expired_guest_access(self):
        """Test access with expired guest token"""
        # Create expired guest access
        guest_access = GuestAccess.objects.create(
            case=self.case,
            access_token="expired_token_123",
            guest_email="guest@test.com",
            permission_type="view",
            created_by=self.instructor,
            expires_at=timezone.now() - timedelta(hours=1),  # Expired
        )

        response = self.client.get("/api/guest-access/expired_token_123/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("expired", response.data["error"].lower())

    def test_extend_guest_access(self):
        """Test extending guest access expiration"""
        guest_access = GuestAccess.objects.create(
            case=self.case,
            access_token="extend_token_123",
            guest_email="guest@test.com",
            permission_type="view",
            created_by=self.instructor,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        self.client.force_authenticate(user=self.instructor)

        original_expires = guest_access.expires_at

        data = {"additional_hours": 24}
        response = self.client.post(
            f"/api/cases/{self.case.id}/guest-access/{guest_access.id}/extend/",  # type: ignore[attr-defined]
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        guest_access.refresh_from_db()
        self.assertGreater(guest_access.expires_at, original_expires)


class CaseGroupAPITests(APITestCase):
    """Test case group API endpoints"""

    def setUp(self):
        self.department = Department.objects.create(name="Pediatrics", code="PED")

        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
            department=self.department,
        )

        self.repository = Repository.objects.create(
            name="Pediatrics Repository", owner=self.instructor
        )

        # Create test cases
        self.cases = []
        for i in range(3):
            case = Case.objects.create(
                title=f"Pediatric Case {i + 1}",
                student=self.instructor,
                repository=self.repository,
                patient_name=f"Patient {i + 1}",
                patient_age=10 + i,
                patient_gender="male" if i % 2 == 0 else "female",
                specialty="Pediatrics",
            )
            self.cases.append(case)

    def test_create_case_group(self):
        """Test creating case group"""
        self.client.force_authenticate(user=self.instructor)

        data = {
            "name": "Pediatric Assignment Week 3",
            "description": "Common pediatric conditions",
            "group_type": "assignment",
            "department": self.department.id,  # type: ignore[attr-defined]
            "class_identifier": "K15PED",
            "add_cases_ids": [case.id for case in self.cases[:2]],
        }

        response = self.client.post("/api/case-groups/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Pediatric Assignment Week 3")
        self.assertEqual(response.data["case_count"], 2)

        # Verify case group created
        case_group = CaseGroup.objects.get(name="Pediatric Assignment Week 3")
        self.assertEqual(case_group.cases.count(), 2)

    def test_grant_permissions_via_group(self):
        """Test granting permissions via case group"""
        # Create case group
        case_group = CaseGroup.objects.create(
            name="Test Assignment",
            created_by=self.instructor,
            department=self.department,
        )
        case_group.cases.add(*self.cases)

        # Create target students
        students = []
        for i in range(2):
            student = User.objects.create_user(  # type: ignore[attr-defined]
                username=f"student{i}@test.com",
                email=f"student{i}@test.com",
                password="testpass123",
                role="student",
            )
            students.append(student)

        self.client.force_authenticate(user=self.instructor)

        data = {
            "target_users": [student.id for student in students],
            "permission_type": "comment",
            "expires_hours": 96,
        }

        response = self.client.post(
            f"/api/case-groups/{case_group.id}/grant-permissions/",  # type: ignore[attr-defined]
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["users_count"], 2)
        self.assertEqual(response.data["cases_count"], 3)

        # Verify permissions created
        for student in students:
            for case in self.cases:
                self.assertTrue(
                    CasePermission.objects.filter(
                        case=case, user=student, permission_type="comment"
                    ).exists()
                )


class UtilityAPITests(APITestCase):
    """Test utility API endpoints"""

    def setUp(self):
        self.instructor = User.objects.create_user(  # type: ignore[attr-defined]
            username="instructor@test.com",
            email="instructor@test.com",
            password="testpass123",
            role="instructor",
        )

        self.student = User.objects.create_user(  # type: ignore[attr-defined]
            username="student@test.com",
            email="student@test.com",
            password="testpass123",
            role="student",
        )

        self.repository = Repository.objects.create(
            name="Test Repository", owner=self.instructor
        )

        self.case = Case.objects.create(
            title="Utility Test Case",
            student=self.instructor,
            repository=self.repository,
            patient_name="Test Patient",
            patient_age=60,
            patient_gender="male",
            specialty="General",
        )

        # Create some shared permissions
        CasePermission.objects.create(
            case=self.case,
            user=self.student,
            permission_type="view",
            granted_by=self.instructor,
        )

    def test_my_shared_cases(self):
        """Test retrieving user's shared cases"""
        self.client.force_authenticate(user=self.student)

        response = self.client.get("/api/my-shared-cases/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 1)
        self.assertEqual(response.data["direct_count"], 1)
        self.assertEqual(len(response.data["shared_cases"]), 1)

    def test_cleanup_expired_permissions(self):
        """Test cleanup of expired permissions"""
        # Create expired permission
        expired_permission = CasePermission.objects.create(
            case=self.case,
            user=self.student,
            permission_type="comment",
            granted_by=self.instructor,
            expires_at=timezone.now() - timedelta(hours=1),
        )

        self.client.force_authenticate(user=self.instructor)

        response = self.client.post("/api/cleanup-expired-permissions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["expired_permissions"], 1)

        # Verify permission marked as inactive
        expired_permission.refresh_from_db()
        self.assertFalse(expired_permission.is_active)

    def test_cleanup_permissions_unauthorized(self):
        """Test cleanup permissions unauthorized access"""
        self.client.force_authenticate(user=self.student)

        response = self.client.post("/api/cleanup-expired-permissions/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
