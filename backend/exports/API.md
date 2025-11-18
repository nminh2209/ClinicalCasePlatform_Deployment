# Export API Documentation

## Base URL
```
http://your-domain.com/api/exports/
```

## Authentication
All endpoints require authentication. Include the token in the header:
```
Authorization: Token YOUR_AUTH_TOKEN
```

---

## Export Templates

### List Export Templates
```
GET /api/exports/templates/
```

**Query Parameters:**
- `type` (optional): Filter by template type
  - Values: `standard`, `academic`, `research`, `clinical`, `presentation`, `anonymized`
- `page` (optional): Page number
- `page_size` (optional): Results per page (max 100)

**Response:**
```json
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Standard Medical Case",
      "vietnamese_name": "Ca Bệnh Chuẩn",
      "template_type": "standard",
      "template_type_display": "Standard Medical Case",
      "is_active": true,
      "is_system_template": true
    }
  ]
}
```

### Get Template Details
```
GET /api/exports/templates/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "Standard Medical Case",
  "vietnamese_name": "Ca Bệnh Chuẩn",
  "description": "Complete case export with all sections",
  "template_type": "standard",
  "template_type_display": "Standard Medical Case",
  "include_patient_details": true,
  "include_medical_history": true,
  "include_examination": true,
  "include_investigations": true,
  "include_diagnosis": true,
  "include_treatment": true,
  "include_learning_objectives": true,
  "include_comments": false,
  "include_attachments": true,
  "include_grades": false,
  "anonymize_patient": false,
  "add_watermark": false,
  "watermark_text": "",
  "header_text": "",
  "footer_text": "",
  "logo_url": "",
  "created_by": null,
  "created_by_name": "",
  "is_active": true,
  "is_system_template": true,
  "created_at": "2025-11-03T10:00:00Z",
  "updated_at": "2025-11-03T10:00:00Z"
}
```

### Create Template (Instructor/Admin only)
```
POST /api/exports/templates/
```

**Request Body:**
```json
{
  "name": "My Custom Template",
  "vietnamese_name": "Mẫu Tùy Chỉnh",
  "description": "Custom template for specific use case",
  "template_type": "academic",
  "include_patient_details": true,
  "include_medical_history": true,
  "include_examination": true,
  "include_investigations": true,
  "include_diagnosis": true,
  "include_treatment": true,
  "include_learning_objectives": true,
  "include_comments": true,
  "include_attachments": true,
  "anonymize_patient": false,
  "add_watermark": true,
  "watermark_text": "EDUCATIONAL USE ONLY"
}
```

**Response:** 201 Created with template details

### Update Template
```
PUT /api/exports/templates/{id}/
PATCH /api/exports/templates/{id}/  # Partial update
```

**Request:** Same as create (all fields for PUT, partial for PATCH)

### Delete Template
```
DELETE /api/exports/templates/{id}/
```

**Note:** System templates cannot be deleted

---

## Case Exports

### List Exports
```
GET /api/exports/case-exports/
```

**Query Parameters:**
- `status`: Filter by status (`pending`, `processing`, `completed`, `failed`, `expired`)
- `format`: Filter by format (`pdf`, `word`, `json`)
- `case`: Filter by case ID
- `start_date`: Filter exports after date (YYYY-MM-DD)
- `end_date`: Filter exports before date (YYYY-MM-DD)
- `page`, `page_size`: Pagination

**Response:**
```json
{
  "count": 50,
  "next": "http://api.example.com/api/exports/case-exports/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "case": 1,
      "case_title": "Acute Respiratory Failure",
      "export_format": "pdf",
      "export_format_display": "PDF Document",
      "status": "completed",
      "status_display": "Completed",
      "file_size": 45678,
      "exported_at": "2025-11-03T14:30:00Z",
      "download_count": 3,
      "expires_at": "2025-12-03T14:30:00Z"
    }
  ]
}
```

### Create Export (Async)
```
POST /api/exports/case-exports/
```

**Request Body:**
```json
{
  "case": 1,
  "export_format": "pdf",
  "template_used": 1,
  "export_settings": {
    "custom_watermark": "CONFIDENTIAL",
    "include_attachments": true
  },
  "expires_at": "2025-12-31T23:59:59Z"
}
```

**Response:** 201 Created
```json
{
  "id": 123,
  "case": 1,
  "case_title": "Acute Respiratory Failure",
  "export_format": "pdf",
  "status": "pending",
  "status_display": "Pending",
  "exported_at": "2025-11-03T14:30:00Z"
}
```

**Note:** The export will be processed asynchronously. Check status with GET request.

### Get Export Details
```
GET /api/exports/case-exports/{id}/
```

**Response:**
```json
{
  "id": 123,
  "case": 1,
  "case_id": 1,
  "case_title": "Acute Respiratory Failure",
  "user": 5,
  "user_name": "John Doe",
  "export_format": "pdf",
  "export_format_display": "PDF Document",
  "status": "completed",
  "status_display": "Completed",
  "file_path": "/media/exports/2025/11/03/case_export_123.pdf",
  "file_url": "http://api.example.com/media/exports/2025/11/03/case_export_123.pdf",
  "file_size": 45678,
  "file_hash": "a1b2c3d4e5f6...",
  "template_used": 1,
  "template_name": "Standard Medical Case",
  "export_settings": {},
  "exported_at": "2025-11-03T14:30:00Z",
  "completed_at": "2025-11-03T14:30:45Z",
  "download_count": 3,
  "last_downloaded_at": "2025-11-03T15:00:00Z",
  "expires_at": "2025-12-03T14:30:00Z",
  "is_expired": false,
  "can_download": true,
  "error_message": "",
  "retry_count": 0
}
```

### Download Export
```
GET /api/exports/case-exports/{id}/download/
```

**Response:** File download (binary data)
- Content-Type: `application/pdf` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `application/json`
- Content-Disposition: `attachment; filename="case_title.ext"`

**Errors:**
- 400: Export not ready (status != completed)
- 404: File not found
- 410: Export expired

### Delete Export
```
DELETE /api/exports/case-exports/{id}/
```

**Response:** 204 No Content

### Get Export Statistics
```
GET /api/exports/case-exports/stats/
```

**Response:**
```json
{
  "total_exports": 150,
  "exports_by_format": {
    "pdf": 80,
    "word": 50,
    "json": 20
  },
  "exports_by_status": {
    "completed": 140,
    "failed": 5,
    "processing": 3,
    "pending": 2
  },
  "total_downloads": 450,
  "total_file_size": 52428800,
  "recent_exports": [
    {
      "id": 150,
      "case_title": "Recent Case",
      "export_format": "pdf",
      "status": "completed",
      "exported_at": "2025-11-03T16:00:00Z"
    }
  ],
  "popular_templates": [
    {
      "template_used__name": "Standard Medical Case",
      "count": 80
    }
  ]
}
```

---

## Batch Exports

### List Batch Exports
```
GET /api/exports/batch-exports/
```

**Query Parameters:**
- `status`: Filter by status (`queued`, `processing`, `completed`, `failed`, `cancelled`)
- `page`, `page_size`: Pagination

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "user": 5,
      "user_name": "John Doe",
      "export_format": "pdf",
      "export_format_display": "PDF Document",
      "status": "completed",
      "status_display": "Completed",
      "total_cases": 10,
      "processed_cases": 10,
      "failed_cases": 0,
      "progress_percentage": 100.0,
      "zip_file_url": "http://api.example.com/media/exports/batch/2025/11/03/batch_1.zip",
      "zip_file_size": 456789,
      "created_at": "2025-11-03T14:00:00Z",
      "completed_at": "2025-11-03T14:05:00Z"
    }
  ]
}
```

### Create Batch Export
```
POST /api/exports/batch-exports/
```

**Request Body:**
```json
{
  "case_ids": [1, 2, 3, 4, 5],
  "export_format": "pdf",
  "template_used": 1,
  "batch_name": "October Cases Backup",
  "compress_output": true,
  "expires_at": "2025-12-31T23:59:59Z"
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "status": "queued",
  "total_cases": 5,
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Note:** Batch export will be processed asynchronously by Celery.

### Get Batch Details
```
GET /api/exports/batch-exports/{id}/
```

**Response:**
```json
{
  "id": 1,
  "user": 5,
  "user_name": "John Doe",
  "cases": [1, 2, 3, 4, 5],
  "case_titles": [
    "Case 1 Title",
    "Case 2 Title",
    "Case 3 Title",
    "Case 4 Title",
    "Case 5 Title"
  ],
  "export_format": "pdf",
  "export_format_display": "PDF Document",
  "template_used": 1,
  "template_name": "Standard Medical Case",
  "batch_name": "October Cases Backup",
  "export_settings": {},
  "compress_output": true,
  "status": "processing",
  "status_display": "Processing",
  "total_cases": 5,
  "processed_cases": 3,
  "failed_cases": 0,
  "progress_percentage": 60.0,
  "zip_file": null,
  "zip_file_url": null,
  "zip_file_size": null,
  "created_at": "2025-11-03T14:00:00Z",
  "started_at": "2025-11-03T14:00:05Z",
  "completed_at": null,
  "expires_at": "2025-12-03T14:00:00Z",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "error_message": ""
}
```

### Download Batch Export
```
GET /api/exports/batch-exports/{id}/download/
```

**Response:** ZIP file download

**Errors:**
- 400: Batch not ready (status != completed)
- 404: File not found

### Cancel Batch Export
```
POST /api/exports/batch-exports/{id}/cancel/
```

**Response:** 200 OK
```json
{
  "status": "Batch export cancelled"
}
```

**Note:** Only queued or processing batches can be cancelled.

### Delete Batch Export
```
DELETE /api/exports/batch-exports/{id}/
```

**Response:** 204 No Content

---

## Quick Export (Synchronous)

### Export to PDF (Instant)
```
GET /api/exports/quick/cases/{case_id}/pdf/
```

**Query Parameters:**
- `template` (optional): Template ID to use

**Response:** Direct PDF file download

### Export to Word (Instant)
```
GET /api/exports/quick/cases/{case_id}/word/
```

**Query Parameters:**
- `template` (optional): Template ID to use

**Response:** Direct Word file download

### Export to JSON (Instant)
```
GET /api/exports/quick/cases/{case_id}/json/
```

**Query Parameters:**
- `template` (optional): Template ID to use

**Response:** Direct JSON file download

**Note:** Quick exports are processed synchronously and return the file immediately. Best for single cases.

---

## Utility Endpoints

### List Export Formats
```
GET /api/exports/formats/
```

**Response:**
```json
[
  {
    "format": "pdf",
    "name": "PDF Document",
    "description": "Professional medical case report in PDF format",
    "supports_vietnamese": true,
    "editable": false,
    "best_for": "Printing, sharing, archival"
  },
  {
    "format": "word",
    "name": "Word Document",
    "description": "Editable Word document (.docx)",
    "supports_vietnamese": true,
    "editable": true,
    "best_for": "Editing, collaboration"
  },
  {
    "format": "json",
    "name": "JSON Data",
    "description": "Structured data export for integration",
    "supports_vietnamese": true,
    "editable": true,
    "best_for": "Data exchange, backup, API integration"
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid export format"
}
```

### 403 Forbidden
```json
{
  "error": "Permission denied. Students can only export their own cases."
}
```

### 404 Not Found
```json
{
  "error": "Case not found"
}
```

### 410 Gone
```json
{
  "error": "Export has expired"
}
```

### 500 Internal Server Error
```json
{
  "error": "Export failed: [error details]"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding:
- Quick exports: 10 per minute per user
- Async exports: 50 per hour per user
- Batch exports: 5 per hour per user

---

## Best Practices

1. **Use Quick Export for single cases** when you need immediate download
2. **Use Async Export for large cases** or when generating multiple exports
3. **Use Batch Export for multiple cases** to get a single ZIP file
4. **Poll status** for async exports until status is 'completed'
5. **Set expiration dates** to prevent storage bloat
6. **Use templates** for consistent formatting
7. **Check can_download** field before attempting download

---

## Examples

### cURL Examples

**Quick PDF Export:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/api/exports/quick/cases/1/pdf/ \
     -o case_export.pdf
```

**Create Async Export:**
```bash
curl -X POST \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"case": 1, "export_format": "pdf", "template_used": 1}' \
     http://localhost:8000/api/exports/case-exports/
```

**Create Batch Export:**
```bash
curl -X POST \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"case_ids": [1,2,3], "export_format": "pdf", "batch_name": "My Batch"}' \
     http://localhost:8000/api/exports/batch-exports/
```

### Python Examples

```python
import requests

# Setup
API_URL = "http://localhost:8000/api/exports"
TOKEN = "your-auth-token"
headers = {"Authorization": f"Token {TOKEN}"}

# Quick Export
response = requests.get(
    f"{API_URL}/quick/cases/1/pdf/",
    headers=headers
)
with open("export.pdf", "wb") as f:
    f.write(response.content)

# Async Export
response = requests.post(
    f"{API_URL}/case-exports/",
    headers=headers,
    json={
        "case": 1,
        "export_format": "pdf",
        "template_used": 1
    }
)
export_id = response.json()["id"]

# Check Status
response = requests.get(
    f"{API_URL}/case-exports/{export_id}/",
    headers=headers
)
status = response.json()["status"]

# Download when ready
if status == "completed":
    response = requests.get(
        f"{API_URL}/case-exports/{export_id}/download/",
        headers=headers
    )
    with open("export.pdf", "wb") as f:
        f.write(response.content)
```

---

## Webhooks (Future Enhancement)

Consider adding webhooks to notify when:
- Export completes
- Batch export completes
- Export fails
- Export expires

---

**Last Updated:** November 3, 2025  
**API Version:** 1.0.0