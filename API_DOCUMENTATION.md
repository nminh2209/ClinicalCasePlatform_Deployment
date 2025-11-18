# Clinical Case Platform API Documentation

## Overview

This document provides comprehensive API documentation for the Clinical Case Platform backend. The API is built with Django REST Framework and uses JWT authentication.

**Base URL:** `http://localhost:8000/api/` (development)  
**Authentication:** JWT Bearer tokens  
**Content-Type:** `application/json`

## Authentication

### Register User
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "role": "student|instructor|admin",
  "password": "password123",
  "password_confirm": "password123"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "role": "student",
    "department": 1,
    "department_name": "Internal Medicine",
    "department_vietnamese_name": "Khoa Nội",
    "specialization": null,
    "student_id": null,
    "employee_id": null
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "message": "User registered successfully"
}
```

### Login
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "role": "student",
    "department": 1,
    "department_name": "Internal Medicine",
    "department_vietnamese_name": "Khoa Nội",
    "specialization": null,
    "student_id": null,
    "employee_id": null
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "message": "Login successful"
}
```

### Refresh Token
```http
POST /api/auth/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "role": "student",
  "department": 1,
  "department_name": "Internal Medicine",
  "department_vietnamese_name": "Khoa Nội",
  "specialization": null,
  "student_id": null,
  "employee_id": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Update User Profile
```http
PUT /api/auth/profile/
PATCH /api/auth/profile/
Authorization: Bearer <access_token>
```

**Request Body (PUT/PATCH):**
```json
{
  "first_name": "Updated First",
  "last_name": "Updated Last",
  "specialization": "Cardiology"
}
```

### List Users
```http
GET /api/auth/users/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `role`: Filter by role (student, instructor, admin)
- `department`: Filter by department ID

**Response (200):**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "full_name": "First Last",
    "role": "student",
    "department": 1,
    "department_name": "Internal Medicine",
    "department_vietnamese_name": "Khoa Nội",
    "specialization": null,
    "student_id": null,
    "employee_id": null
  }
]
```

## Cases API

### List Cases
```http
GET /api/cases/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `specialty`: Filter by specialty
- `case_status`: Filter by status (draft, submitted, reviewed, approved)
- `priority_level`: Filter by priority (low, medium, high, urgent)
- `complexity_level`: Filter by complexity (basic, intermediate, advanced, expert)
- `date_from`: Filter cases created after date (YYYY-MM-DD)
- `date_to`: Filter cases created before date (YYYY-MM-DD)
- `admission_from`: Filter by admission date after (YYYY-MM-DD)
- `admission_to`: Filter by admission date before (YYYY-MM-DD)
- `department`: Filter by department ID
- `search`: Search in title, diagnosis, patient_name, keywords
- `q`: Alternative search parameter
- `is_public`: Filter public cases (true/false)
- `ordering`: Order by (created_at, updated_at, title, priority_level, admission_date)
- `page`: Page number for pagination
- `page_size`: Items per page (default: 20, max: 100)

**Response (200):**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/cases/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Case Title",
      "patient_name": "Patient Name",
      "case_status": "draft",
      "priority_level": "medium",
      "complexity_level": "intermediate",
      "specialty": "Internal Medicine",
      "diagnosis": "Diagnosis",
      "case_summary": "Summary",
      "keywords": "keyword1, keyword2",
      "is_public": false,
      "admission_date": "2024-01-01",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "student": {
        "id": 1,
        "full_name": "Student Name",
        "department_name": "Internal Medicine"
      },
      "repository": {
        "id": 1,
        "name": "Repository Name"
      },
      "comment_count": 5
    }
  ]
}
```

### Create Case
```http
POST /api/cases/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Case Title",
  "patient_name": "Patient Name",
  "case_status": "draft",
  "priority_level": "medium",
  "complexity_level": "intermediate",
  "specialty": "Internal Medicine",
  "diagnosis": "Diagnosis",
  "case_summary": "Summary",
  "keywords": "keyword1, keyword2",
  "is_public": false,
  "admission_date": "2024-01-01",
  "repository": 1,
  "clinical_history": {
    "chief_complaint": "Chief complaint",
    "history_present_illness": "HPI",
    "past_medical_history": "PMH",
    "family_history": "FH",
    "social_history": "SH",
    "allergies": "Allergies",
    "medications": "Medications",
    "review_systems": "ROS"
  },
  "physical_examination": {
    "general_appearance": "GA",
    "vital_signs": "VS",
    "head_neck": "HEENT",
    "cardiovascular": "CV",
    "respiratory": "Resp",
    "abdominal": "Abd",
    "neurological": "Neuro",
    "musculoskeletal": "MSK",
    "skin": "Skin",
    "other_systems": "Other"
  },
  "investigations": {
    "laboratory_results": "Labs",
    "imaging_studies": "Imaging",
    "ecg_findings": "ECG",
    "pathology_results": "Pathology",
    "special_tests": "Special tests",
    "microbiology": "Micro",
    "biochemistry": "Biochem",
    "hematology": "Heme"
  },
  "diagnosis_management": {
    "primary_diagnosis": "Primary Dx",
    "differential_diagnosis": "DDx",
    "management_plan": "Management",
    "treatment": "Treatment",
    "follow_up": "Follow-up",
    "prognosis": "Prognosis",
    "complications": "Complications"
  },
  "learning_outcomes": {
    "learning_objectives": "Objectives",
    "key_learning_points": "Key points",
    "clinical_pearls": "Pearls",
    "references": "References"
  }
}
```

### Get Case Detail
```http
GET /api/cases/{id}/
Authorization: Bearer <access_token>
```

**Response (200):** Returns detailed case information including all nested data.

### Update Case
```http
PUT /api/cases/{id}/
PATCH /api/cases/{id}/
Authorization: Bearer <access_token>
```

**Request Body:** Same as create, but all fields optional for PATCH.

### Delete Case
```http
DELETE /api/cases/{id}/
Authorization: Bearer <access_token>
```

**Response (204):** No content

### Submit Case for Review
```http
POST /api/cases/{id}/submit/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Case submitted for review successfully"
}
```

## Case Permissions API

### List Case Permissions
```http
GET /api/cases/{case_id}/permissions/
Authorization: Bearer <access_token>
```

### Create Case Permission
```http
POST /api/cases/{case_id}/permissions/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "user": 2,
  "share_type": "individual|department|public",
  "target_department": 1,  // Only for department share_type
  "can_view": true,
  "can_edit": false,
  "can_export": true,
  "expires_at": "2024-12-31T23:59:59Z"  // Optional
}
```

### Bulk Grant Permissions
```http
POST /api/cases/{case_id}/permissions/bulk-grant/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "users": [2, 3, 4],
  "share_type": "individual",
  "can_view": true,
  "can_edit": false,
  "can_export": true,
  "expires_at": "2024-12-31T23:59:59Z"
}
```

### Bulk Revoke Permissions
```http
POST /api/cases/{case_id}/permissions/bulk-revoke/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "users": [2, 3, 4]
}
```

### Permission Audit Log
```http
GET /api/cases/{case_id}/permissions/audit-log/
Authorization: Bearer <access_token>
```

## Guest Access API

### List Guest Access
```http
GET /api/cases/{case_id}/guest-access/
Authorization: Bearer <access_token>
```

### Create Guest Access
```http
POST /api/cases/{case_id}/guest-access/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "guest_name": "Dr. Smith",
  "guest_email": "smith@example.com",
  "can_view": true,
  "can_export": false,
  "expires_at": "2024-12-31T23:59:59Z"
}
```

### Extend Guest Access
```http
POST /api/cases/{case_id}/guest-access/{id}/extend/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "expires_at": "2024-12-31T23:59:59Z"
}
```

### Public Guest Access (No Auth Required)
```http
GET /api/guest-access/{access_token}/
```

## Medical Attachments API

### List Case Attachments
```http
GET /api/cases/{case_id}/attachments/
Authorization: Bearer <access_token>
```

### Upload Attachment
```http
POST /api/cases/{case_id}/attachments/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: File to upload
- `attachment_type`: document|image|video|audio
- `description`: Optional description

### Get Attachment Detail
```http
GET /api/cases/attachments/{id}/
Authorization: Bearer <access_token>
```

### Delete Attachment
```http
DELETE /api/cases/attachments/{id}/
Authorization: Bearer <access_token>
```

## Student Notes API

### List Case Notes
```http
GET /api/cases/{case_id}/notes/
Authorization: Bearer <access_token>
```

### Create Note
```http
POST /api/cases/{case_id}/notes/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "content": "Note content",
  "note_type": "reflection|question|observation",
  "is_private": false
}
```

### Update Note
```http
PUT /api/cases/notes/{id}/
PATCH /api/cases/notes/{id}/
Authorization: Bearer <access_token>
```

### Delete Note
```http
DELETE /api/cases/notes/{id}/
Authorization: Bearer <access_token>
```

## Departments API

### List Departments
```http
GET /api/cases/departments/
Authorization: Bearer <access_token>
```

### Create Department
```http
POST /api/cases/departments/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Internal Medicine",
  "vietnamese_name": "Khoa Nội",
  "code": "IM",
  "description": "Internal Medicine Department",
  "is_active": true
}
```

### Get Department Detail
```http
GET /api/cases/departments/{id}/
Authorization: Bearer <access_token>
```

### Update Department
```http
PUT /api/cases/departments/{id}/
PATCH /api/cases/departments/{id}/
Authorization: Bearer <access_token>
```

### Delete Department
```http
DELETE /api/cases/departments/{id}/
Authorization: Bearer <access_token>
```

## Terminology API

### List Medical Terms
```http
GET /api/cases/terminology/terms/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search term
- `category`: Filter by category

### Create Medical Term
```http
POST /api/cases/terminology/terms/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "term": "Myocardial Infarction",
  "definition": "Heart attack",
  "vietnamese_term": "Nhồi máu cơ tim",
  "vietnamese_definition": "Đột quỵ tim",
  "category": "cardiology",
  "abbreviations": ["MI", "STEMI", "NSTEMI"]
}
```

### Autocomplete Terms
```http
GET /api/cases/terminology/terms/autocomplete/?q=myocardial
Authorization: Bearer <access_token>
```

### List ICD-10 Codes
```http
GET /api/cases/terminology/icd10/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Search in code or description

### List Abbreviations
```http
GET /api/cases/terminology/abbreviations/
Authorization: Bearer <access_token>
```

### Create Abbreviation
```http
POST /api/cases/terminology/abbreviations/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "abbreviation": "MI",
  "full_form": "Myocardial Infarction",
  "vietnamese_full_form": "Nhồi máu cơ tim",
  "category": "cardiology"
}
```

## Exports API

### Quick Export PDF
```http
GET /api/exports/quick/cases/{case_id}/pdf/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `template`: Template ID to use (optional)

**Response:** PDF file download

### Quick Export Word
```http
GET /api/exports/quick/cases/{case_id}/word/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `template`: Template ID to use (optional)

**Response:** Word document download

### Quick Export JSON
```http
GET /api/exports/quick/cases/{case_id}/json/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `template`: Template ID to use (optional)

**Response:** JSON file download

### Legacy Export Endpoints (Deprecated)
```http
GET /api/exports/cases/{case_id}/pdf/
GET /api/exports/cases/{case_id}/word/
GET /api/exports/cases/{case_id}/json/
Authorization: Bearer <access_token>
```

### Export Templates
```http
GET /api/exports/templates/
POST /api/exports/templates/
Authorization: Bearer <access_token>
```

### Batch Exports
```http
GET /api/exports/batch-exports/
POST /api/exports/batch-exports/
Authorization: Bearer <access_token>
```

**Request Body for Batch Export:**
```json
{
  "name": "Batch Export Name",
  "cases": [1, 2, 3],
  "export_format": "pdf|word|json",
  "template": 1  // Optional
}
```

### Export Formats
```http
GET /api/exports/formats/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "formats": ["pdf", "word", "json"],
  "descriptions": {
    "pdf": "Portable Document Format",
    "word": "Microsoft Word Document",
    "json": "JavaScript Object Notation"
  }
}
```

## Comments API

### List Comments
```http
GET /api/comments/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `case`: Filter by case ID
- `author`: Filter by author ID

### Create Comment
```http
POST /api/comments/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "case": 1,
  "content": "This is a comment",
  "parent": null  // For replies, set to parent comment ID
}
```

### Get Comment Detail
```http
GET /api/comments/{id}/
Authorization: Bearer <access_token>
```

### Update Comment
```http
PUT /api/comments/{id}/
PATCH /api/comments/{id}/
Authorization: Bearer <access_token>
```

### Delete Comment
```http
DELETE /api/comments/{id}/
Authorization: Bearer <access_token>
```

## Feedback API

### List Feedback
```http
GET /api/feedback/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `case`: Filter by case ID
- `reviewer`: Filter by reviewer ID

### Create Feedback
```http
POST /api/feedback/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "case": 1,
  "content": "Feedback content",
  "rating": 4,
  "feedback_type": "general|clinical|educational"
}
```

### Get Feedback Detail
```http
GET /api/feedback/{id}/
Authorization: Bearer <access_token>
```

### Update Feedback
```http
PUT /api/feedback/{id}/
PATCH /api/feedback/{id}/
Authorization: Bearer <access_token>
```

### Delete Feedback
```http
DELETE /api/feedback/{id}/
Authorization: Bearer <access_token>
```

## Grades API

### List Grades
```http
GET /api/grades/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `case`: Filter by case ID
- `student`: Filter by student ID
- `grader`: Filter by grader ID

### Create Grade
```http
POST /api/grades/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "case": 1,
  "student": 2,
  "grade": 85.5,
  "max_grade": 100,
  "comments": "Good work",
  "criteria": {
    "clinical_reasoning": 8,
    "data_interpretation": 9,
    "management_plan": 8,
    "communication": 9
  }
}
```

### Get Grade Detail
```http
GET /api/grades/{id}/
Authorization: Bearer <access_token>
```

### Update Grade
```http
PUT /api/grades/{id}/
PATCH /api/grades/{id}/
Authorization: Bearer <access_token>
```

### Delete Grade
```http
DELETE /api/grades/{id}/
Authorization: Bearer <access_token>
```

## Repositories API

### List Repositories
```http
GET /api/repositories/
Authorization: Bearer <access_token>
```

### Create Repository
```http
POST /api/repositories/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Internal Medicine Cases",
  "description": "Repository for internal medicine cases",
  "department": 1,
  "is_public": false,
  "allow_student_submissions": true
}
```

### Get Repository Detail
```http
GET /api/repositories/{id}/
Authorization: Bearer <access_token>
```

### Update Repository
```http
PUT /api/repositories/{id}/
PATCH /api/repositories/{id}/
Authorization: Bearer <access_token>
```

### Delete Repository
```http
DELETE /api/repositories/{id}/
Authorization: Bearer <access_token>
```

## Templates API

### List Case Templates
```http
GET /api/templates/
Authorization: Bearer <access_token>
```

### Create Case Template
```http
POST /api/templates/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Standard Case Template",
  "description": "Template for standard clinical cases",
  "department": 1,
  "template_data": {
    "sections": ["clinical_history", "physical_exam", "investigations", "diagnosis_management"],
    "required_fields": ["title", "diagnosis", "case_summary"]
  },
  "is_default": false
}
```

### Get Template Detail
```http
GET /api/templates/{id}/
Authorization: Bearer <access_token>
```

### Update Template
```http
PUT /api/templates/{id}/
PATCH /api/templates/{id}/
Authorization: Bearer <access_token>
```

### Delete Template
```http
DELETE /api/templates/{id}/
Authorization: Bearer <access_token>
```

## Case Groups API

### List Case Groups
```http
GET /api/case-groups/
Authorization: Bearer <access_token>
```

### Create Case Group
```http
POST /api/case-groups/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Cardiology Cases",
  "description": "Group of cardiology cases",
  "department": 1,
  "cases": [1, 2, 3],
  "is_public": false
}
```

### Get Case Group Detail
```http
GET /api/case-groups/{id}/
Authorization: Bearer <access_token>
```

### Update Case Group
```http
PUT /api/case-groups/{id}/
PATCH /api/case-groups/{id}/
Authorization: Bearer <access_token>
```

### Delete Case Group
```http
DELETE /api/case-groups/{id}/
Authorization: Bearer <access_token>
```

## Shared Cases API

### Get My Shared Cases
```http
GET /api/my-shared-cases/
Authorization: Bearer <access_token>
```

### Get Accessible Cases
```http
GET /api/accessible-cases/
Authorization: Bearer <access_token>
```

### Cleanup Expired Permissions
```http
POST /api/cleanup-expired-permissions/
Authorization: Bearer <access_token>
```

## API Documentation

### Swagger UI
```
GET /api/docs/
```

### ReDoc
```
GET /api/redoc/
```

### OpenAPI Schema
```
GET /api/schema/
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Rate Limiting

- Authenticated requests: 1000/hour
- Unauthenticated requests: 100/hour
- Export requests: 50/hour per user

## Pagination

List endpoints return paginated results:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

Default page size: 20, maximum: 100

## Filtering and Search

Most list endpoints support filtering and search. Check individual endpoint documentation for available parameters.

## Authentication Headers

Include the JWT access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## File Uploads

For file uploads, use `Content-Type: multipart/form-data` and include the file in the request body.

## Date Formats

All dates should be in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

## Common Query Parameters

- `page`: Page number for pagination
- `page_size`: Number of items per page
- `ordering`: Field to order by (prefix with `-` for descending)
- `search`: Search query
- `q`: Alternative search query</content>
<parameter name="filePath">/home/zilus/Desktop/SwinCode/Sem7/HN2.1ProjectA/API_DOCUMENTATION.md