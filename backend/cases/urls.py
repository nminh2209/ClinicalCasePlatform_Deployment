from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaseListCreateView,
    CaseDetailView,
    CasePermissionListCreateView,
    MedicalAttachmentListCreateView,
    MedicalAttachmentDetailView,
    StudentNotesListCreateView,
    StudentNotesDetailView,
    DepartmentListCreateView,
    DepartmentDetailView,
    submit_case_for_review,
    review_case,
    approve_case,
    reject_case,
    revoke_case_permission,
    check_case_permission,
    # Enhanced permission management views
    EnhancedCasePermissionViewSet,
    GuestAccessViewSet,
    # CaseGroupViewSet, # Now imported in main urls.py
    guest_access_case,
    my_shared_cases,
    accessible_cases,
    cleanup_expired_permissions,
    MedicalTermListCreateView,
    MedicalTermRetrieveUpdateDestroyView,
    MedicalTermAutocompleteView,
    ICD10ListView,
    AbbreviationListCreateView,
    case_summary_view,
)

# Public Feed Views
from .feed_views import (
    PublicFeedListView,
    PublicFeedDetailView,
    publish_to_feed,
    unpublish_from_feed,
    react_to_case,
    remove_reaction,
    get_case_reactions,
    feed_statistics,
)

# Router for ViewSets - case-groups now handled at main level
# router = DefaultRouter()
# router.register(r'case-groups', CaseGroupViewSet, basename='case-groups')

urlpatterns = [
    # Include router URLs - removed case-groups (now at main level)
    # path('', include(router.urls)),
    # Departments
    path("departments/", DepartmentListCreateView.as_view(), name="department-list"),
    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    # Case CRUD
    path("", CaseListCreateView.as_view(), name="case-list-create"),
    path("<int:pk>/", CaseDetailView.as_view(), name="case-detail"),
    # Enhanced Permission Management System
    # Case Permissions (Enhanced)
    path(
        "<int:case_pk>/permissions/",
        EnhancedCasePermissionViewSet.as_view({"get": "list", "post": "create"}),
        name="case-permissions-enhanced",
    ),
    path(
        "<int:case_pk>/permissions/<int:pk>/",
        EnhancedCasePermissionViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="case-permission-detail",
    ),
    path(
        "<int:case_pk>/permissions/bulk-grant/",
        EnhancedCasePermissionViewSet.as_view({"post": "bulk_grant"}),
        name="bulk-grant-permissions",
    ),
    path(
        "<int:case_pk>/permissions/bulk-revoke/",
        EnhancedCasePermissionViewSet.as_view({"post": "bulk_revoke"}),
        name="bulk-revoke-permissions",
    ),
    path(
        "<int:case_pk>/permissions/audit-log/",
        EnhancedCasePermissionViewSet.as_view({"get": "audit_log"}),
        name="permission-audit-log",
    ),
    # Guest Access Management
    path(
        "<int:case_pk>/guest-access/",
        GuestAccessViewSet.as_view({"get": "list", "post": "create"}),
        name="guest-access-list",
    ),
    path(
        "<int:case_pk>/guest-access/<int:pk>/",
        GuestAccessViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="guest-access-detail",
    ),
    path(
        "<int:case_pk>/guest-access/<int:pk>/extend/",
        GuestAccessViewSet.as_view({"post": "extend"}),
        name="extend-guest-access",
    ),
    # Public Guest Access (no auth required)
    path(
        "guest-access/<str:access_token>/", guest_access_case, name="guest-access-case"
    ),
    # User's shared cases
    path("my-shared-cases/", my_shared_cases, name="my-shared-cases"),
    path("accessible-cases/", accessible_cases, name="accessible-cases"),
    # Admin utilities
    path(
        "cleanup-expired-permissions/",
        cleanup_expired_permissions,
        name="cleanup-expired-permissions",
    ),
    # Legacy Case permissions (backward compatibility)
    path(
        "<int:case_pk>/permissions/legacy/",
        CasePermissionListCreateView.as_view(),
        name="case-permissions-legacy",
    ),
    path(
        "<int:case_pk>/permissions/<int:permission_id>/revoke/",
        revoke_case_permission,
        name="revoke-permission-legacy",
    ),
    path(
        "<int:pk>/check-permission/",
        check_case_permission,
        name="check-permission",
    ),
    # Medical attachments
    path(
        "<int:case_pk>/attachments/",
        MedicalAttachmentListCreateView.as_view(),
        name="case-attachments",
    ),
    path(
        "attachments/<int:pk>/",
        MedicalAttachmentDetailView.as_view(),
        name="attachment-detail",
    ),
    # Case actions
    path("<int:pk>/submit/", submit_case_for_review, name="case-submit"),
    path("<int:pk>/review/", review_case, name="case-review"),
    path("<int:pk>/approve/", approve_case, name="case-approve"),
    path("<int:pk>/reject/", reject_case, name="case-reject"),
    # Student notes
    path(
        "<int:case_id>/notes/",
        StudentNotesListCreateView.as_view(),
        name="student-notes-list",
    ),
    path(
        "notes/<int:id>/",
        StudentNotesDetailView.as_view(),
        name="student-notes-detail",
    ),
    # Terminology endpoints
    path(
        "terminology/terms/",
        MedicalTermListCreateView.as_view(),
        name="terminology-terms",
    ),
    path(
        "terminology/terms/<int:pk>/",
        MedicalTermRetrieveUpdateDestroyView.as_view(),
        name="terminology-term-detail",
    ),
    path(
        "terminology/terms/autocomplete/",
        MedicalTermAutocompleteView.as_view(),
        name="terminology-terms-autocomplete",
    ),
    path("terminology/icd10/", ICD10ListView.as_view(), name="terminology-icd10"),
    path(
        "terminology/abbreviations/",
        AbbreviationListCreateView.as_view(),
        name="terminology-abbreviations",
    ),
    
    # Public Feed / Social Media endpoints
    path("public-feed/", PublicFeedListView.as_view(), name="public-feed-list"),
    path("public-feed/<int:pk>/", PublicFeedDetailView.as_view(), name="public-feed-detail"),
    path("<int:pk>/publish-to-feed/", publish_to_feed, name="publish-to-feed"),
    path("<int:pk>/unpublish-from-feed/", unpublish_from_feed, name="unpublish-from-feed"),
    path("<int:pk>/react/", react_to_case, name="react-to-case"),
    path("<int:pk>/reactions/", get_case_reactions, name="case-reactions"),
    path("feed-statistics/", feed_statistics, name="feed-statistics"),
    
    # Case Summary / Analytics
    path("summary/", case_summary_view, name="case-summary"),
]
