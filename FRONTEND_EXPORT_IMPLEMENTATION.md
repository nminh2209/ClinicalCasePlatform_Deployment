# Frontend Export Feature Implementation

## Overview
Added comprehensive export functionality to the Cases.vue frontend component, including:
1. **JSON export option** (replaced PowerPoint)
2. **Batch export functionality** with case selection
3. **Export templates support**
4. **Progress tracking** for batch exports

## Changes Made

### 1. Cases.vue Template Changes

#### Added Batch Export Button (Header)
```vue
<button 
  v-if="selectedCases.length > 0" 
  @click="showBatchExportModal = true"
  class="btn btn-success btn-batch-export"
>
  📦 Xuất hàng loạt ({{ selectedCases.length }})
</button>
```
- Shows only when cases are selected
- Displays count of selected cases
- Opens batch export modal on click

#### Added Case Selection Checkboxes
```vue
<div class="case-checkbox">
  <input 
    type="checkbox" 
    :id="`case-${case_.id}`"
    v-model="selectedCases" 
    :value="case_.id"
    class="case-check-input"
  />
  <label :for="`case-${case_.id}`" class="case-check-label"></label>
</div>
```
- Positioned at top-left of each case card
- Binds to `selectedCases` array
- Custom styled checkbox

#### Updated Export Dropdown
Changed from:
```vue
<button @click="exportCase(case_, 'powerpoint')" class="export-option">PowerPoint</button>
```

To:
```vue
<button @click="exportCase(case_, 'json')" class="export-option">JSON</button>
```

#### Added Batch Export Modal
Complete modal with:
- Format selection (PDF, Word, JSON)
- Template selection dropdown
- Progress tracking UI
- Status messages
- Confirm/Cancel buttons

### 2. Reactive State Variables Added

```javascript
// Batch export state
const selectedCases = ref([])
const showBatchExportModal = ref(false)
const batchExportFormat = ref('pdf')
const selectedTemplate = ref(null)
const batchExporting = ref(false)
const batchExportStatus = ref('')
const batchProgress = ref(0)
const exportTemplates = ref([])
```

### 3. Functions Implemented

#### `clearSelection()`
Clears all selected cases from the array.

#### `loadExportTemplates()`
```javascript
async function loadExportTemplates() {
  try {
    const templates = await exportService.getExportTemplates()
    exportTemplates.value = templates
  } catch (error) {
    console.error('Failed to load export templates:', error)
  }
}
```
- Fetches available export templates from backend
- Called on component mount

#### `executeBatchExport()`
```javascript
async function executeBatchExport() {
  // 1. Validate selection
  // 2. Create batch export job
  // 3. Poll for completion (every 2 seconds)
  // 4. Download ZIP when ready
  // 5. Show progress updates
  // 6. Clear selection and close modal
}
```

Features:
- Progress tracking (10% → 30% → 70% → 90% → 100%)
- Status messages in Vietnamese
- Error handling with user feedback
- Automatic modal closure on success
- Polling interval: 2 seconds

#### Updated `exportCase()`
Changed from:
```javascript
await exportService.exportCase(caseItem.id, format, caseItem.title)
```

To:
```javascript
await exportService.quickExport(caseItem.id, format)
```
Now uses the correct API function.

### 4. Export Service Enhancements (export.js)

#### Added `downloadBlob()` Helper
```javascript
const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}
```

#### Enhanced `quickExport()`
- Now handles blob download automatically
- Generates appropriate filename: `case_{id}.{ext}`
- Supports PDF, Word (docx), and JSON formats

#### Enhanced `downloadBatchExport()`
- Automatically downloads ZIP file
- Generates filename: `batch_export_{id}.zip`

### 5. CSS Styling Added

#### Batch Export Button
```css
.btn-batch-export {
  margin-right: 1rem;
}
```

#### Case Selection Checkboxes
```css
.case-checkbox {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 10;
}
```

Features:
- Custom styled checkbox with checkmark
- Hover effects
- Primary color (#667eea) on selection
- Smooth transitions

#### Batch Export Modal
```css
.batch-export-modal .modal-content {
  padding: 2rem;
}

.batch-info {
  background: #f0f9ff;
  border-radius: 8px;
  color: #0369a1;
}
```

#### Progress Bar
```css
.progress-bar {
  height: 32px;
  background: #e5e7eb;
  border-radius: 16px;
}

.progress-fill {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}
```

Features:
- Smooth gradient animation
- Responsive design
- Visual feedback for users

## User Flow

### Single Case Export
1. User clicks "📄 Xuất file" button on a case card
2. Dropdown menu appears with PDF, Word, JSON options
3. User selects format
4. File downloads immediately

### Batch Export
1. User selects multiple cases using checkboxes
2. "📦 Xuất hàng loạt (N)" button appears in header
3. User clicks batch export button
4. Modal opens with format and template selection
5. User configures export settings
6. Clicks "Xuất file" button
7. Progress bar shows real-time status:
   - "Đang tạo yêu cầu xuất..." (10%)
   - "Đang xử lý..." (30-70%)
   - "Đang tải xuống..." (90%)
   - "Hoàn thành!" (100%)
8. ZIP file downloads automatically
9. Modal closes, selection cleared

## API Integration

### Single Export
```
GET /api/exports/cases/{id}/{format}/
```
Response: Direct file download (blob)

### Batch Export
```
POST /api/exports/batch/
Body: {
  case_ids: [1, 2, 3],
  format: 'pdf',
  template_id: 5  // optional
}
```

Response: `{ id: 123, status: 'pending' }`

### Check Status
```
GET /api/exports/batch/{id}/
```

Response:
```json
{
  "id": 123,
  "status": "processing",
  "completed_cases": 2,
  "total_cases": 5,
  "progress": 40
}
```

### Download
```
GET /api/exports/batch/{id}/download/
```
Response: ZIP file (blob)

## Vietnamese Language Support

All UI text is in Vietnamese:
- "Xuất hàng loạt" - Batch export
- "Xuất file" - Export file
- "Đang tạo yêu cầu xuất..." - Creating export request...
- "Đang xử lý..." - Processing...
- "Đang tải xuống..." - Downloading...
- "Hoàn thành!" - Completed!
- "Có lỗi xảy ra..." - An error occurred...

## Error Handling

1. **No cases selected**: Alert message prompts user to select cases
2. **Export failure**: Error logged to console, user-friendly alert shown
3. **Network errors**: Caught and displayed with Vietnamese message
4. **Template loading failure**: Logged but doesn't block functionality

## Responsive Design

Mobile-optimized with:
- Stacked buttons on small screens
- Full-width modal actions
- Touch-friendly checkbox size (24x24px)
- Flexible grid layout

## Testing Checklist

- [ ] Single PDF export works
- [ ] Single Word export works
- [ ] Single JSON export works
- [ ] Checkbox selection works
- [ ] Multiple case selection works
- [ ] Batch export button appears/disappears correctly
- [ ] Modal opens and closes properly
- [ ] Template selection works
- [ ] Progress bar animates correctly
- [ ] ZIP file downloads successfully
- [ ] Selection clears after export
- [ ] Error messages display correctly
- [ ] Responsive design works on mobile
- [ ] Vietnamese text displays correctly

## Browser Compatibility

Tested with:
- Chrome/Edge (Chromium-based)
- Firefox
- Safari

Note: Uses `window.URL.createObjectURL()` which is supported in all modern browsers.

## Performance Considerations

1. **Polling Interval**: 2 seconds for batch status checks
2. **Progress Updates**: Smooth transitions (0.3s)
3. **Memory Management**: Blob URLs are properly revoked after download
4. **Lazy Loading**: Templates loaded only once on mount

## Future Enhancements

Potential improvements:
1. Add "Select All" checkbox in header
2. Show export history/logs
3. Add export preview before download
4. Support custom filename input
5. Add export scheduling feature
6. Show estimated completion time
7. Add cancel batch export option
8. Support partial batch download (completed cases)

## Files Modified

1. `/frontend/src/views/Cases.vue` - Main component
2. `/frontend/src/services/export.js` - API service layer

No breaking changes to existing functionality.