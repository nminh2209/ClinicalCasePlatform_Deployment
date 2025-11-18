# 🌐 Social Media Feed - User Guide

## Overview
The Social Media Feed allows instructors to publish high-quality student cases to a public feed where other students can view, react, and learn from exemplary clinical cases.

---

## 📋 Workflow

### For Students:
1. **Create Case** → Submit clinical case as usual
2. **Wait for Approval** → Instructor reviews and approves
3. **View on Feed** → If published by instructor, appears on public feed
4. **Engage** → React and comment on published cases

### For Instructors:
1. **Review Cases** → Approve high-quality student cases
2. **Publish to Feed** → Share approved cases publicly
3. **Manage Visibility** → Control department-only or university-wide
4. **Feature Cases** → Highlight exceptional cases

---

## 👨‍🏫 How to Publish Cases to Feed (Instructors)

### Method 1: Through Django Admin Panel

1. **Access Admin Panel:**
   ```
   http://localhost:8000/admin/
   ```

2. **Navigate to Cases:**
   - Click on "Cases" → "Cases" in the sidebar

3. **Find Approved Case:**
   - Filter by `approval_status = "approved"`
   - Look for high-quality cases worth sharing

4. **Publish to Feed:**
   - Click on the case to edit
   - Scroll to **"Social Media Feed Settings"** section
   - Check ✅ **"Is published to feed"**
   - Set **"Feed visibility"**: 
     - `Department` - Only students in same department
     - `University` - All students can see
   - Check ✅ **"Is featured"** (optional - for exceptional cases)
   - Click **"Save"**

### Method 2: Through API (Programmatic)

**Endpoint:** `POST /api/cases/{case_id}/publish-to-feed/`

**Request Body:**
```json
{
  "feed_visibility": "department",  // or "university"
  "is_featured": false              // or true
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/cases/123/publish-to-feed/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"feed_visibility": "department", "is_featured": false}'
```

**Example using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/cases/123/publish-to-feed/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'feed_visibility': 'university',
        'is_featured': True
    }
)
```

---

## 👨‍🎓 How to View and Interact with Feed (Students & Instructors)

### Accessing the Public Feed

1. **Login to Application:**
   ```
   http://localhost:5173
   ```

2. **Navigate to Public Feed:**
   - Click **"Bệnh Án Công Khai"** (🌐 icon) in the sidebar
   - Or go directly to: `http://localhost:5173/public-feed`

### Feed Filters

**Filter by Visibility:**
- 🏢 **Khoa của tôi** - Cases from your department only
- 🌐 **Tất cả** - All published cases (university-wide)
- ⭐ **Nổi bật** - Featured cases only

**Filter by Specialty:**
- Use dropdown to select: Nội khoa, Ngoại khoa, Tim mạch, etc.

### Reacting to Cases

Click on reaction buttons to show appreciation:
- 👍 **Thích** (Like) - General appreciation
- ❤️ **Yêu thích** (Love) - Really valuable case
- 💡 **Hữu ích** (Insightful) - Learned something new
- 📚 **Học được** (Learned) - Educational value

**Note:** You can only have ONE reaction per case. Clicking the same reaction again removes it.

### Viewing Full Case

- Click **"Xem đầy đủ"** (👁️ View Full) button
- Opens complete case details with all medical information

---

## 🔧 API Endpoints Reference

### Feed Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cases/public-feed/` | List published cases | ✅ Yes |
| GET | `/api/cases/public-feed/{id}/` | Get single published case | ✅ Yes |
| POST | `/api/cases/{id}/publish-to-feed/` | Publish case (instructor only) | ✅ Instructor |
| POST | `/api/cases/{id}/unpublish-from-feed/` | Remove from feed (instructor only) | ✅ Instructor |
| POST | `/api/cases/{id}/react/` | Add/update reaction | ✅ Yes |
| DELETE | `/api/cases/{id}/react/` | Remove reaction | ✅ Yes |
| GET | `/api/cases/{id}/reactions/` | Get reaction summary | ✅ Yes |
| GET | `/api/cases/feed-statistics/` | Get feed statistics | ✅ Yes |

### Query Parameters for `/api/cases/public-feed/`

```
GET /api/cases/public-feed/?filter=department&specialty=Nội%20khoa&page=1
```

| Parameter | Type | Description | Options |
|-----------|------|-------------|---------|
| `filter` | string | Visibility filter | `all`, `department`, `featured` |
| `specialty` | string | Medical specialty | Any specialty name |
| `page` | integer | Page number | 1, 2, 3... |
| `page_size` | integer | Items per page | Default: 10 |

---

## 💡 Best Practices

### For Instructors Publishing Cases:

1. **Quality Control:**
   - Only publish cases that are complete and accurate
   - Ensure patient privacy is maintained
   - Verify all medical information is correct

2. **Visibility Settings:**
   - Use `department` for department-specific learning
   - Use `university` for exceptional cases with broad educational value

3. **Featured Cases:**
   - Reserve ⭐ featured status for truly exceptional cases
   - Use sparingly to maintain significance

4. **Timing:**
   - Publish cases after thorough review
   - Consider publishing as teaching materials after grading

### For Students Using the Feed:

1. **Active Learning:**
   - Read cases thoroughly before reacting
   - Use different reaction types appropriately
   - Comment to ask questions or share insights

2. **Engagement:**
   - React to cases you find valuable
   - Help others learn by sharing your understanding
   - Respect confidentiality and professional standards

---

## 🎯 Quick Start Examples

### Example 1: Instructor Publishing a Case

**Scenario:** You've reviewed an excellent cardiology case and want to share it with all students.

**Steps:**
1. Go to http://localhost:8000/admin/
2. Navigate to Cases → find the case
3. Edit the case:
   - ✅ Is published to feed
   - Feed visibility: `University`
   - ✅ Is featured (because it's exceptional)
4. Save

**Result:** Case appears on public feed for all students with ⭐ featured badge.

### Example 2: Student Viewing and Reacting

**Scenario:** You want to learn from published cases in your department.

**Steps:**
1. Go to http://localhost:5173/public-feed
2. Click **"Khoa của tôi"** filter
3. Browse cases from your department
4. Click 💡 **"Hữu ích"** on insightful cases
5. Click **"Xem đầy đủ"** to see complete details

**Result:** You've engaged with quality cases and contributed to the learning community.

### Example 3: Unpublishing a Case

**Scenario:** A case needs to be removed from the feed.

**API Request:**
```bash
curl -X POST http://localhost:8000/api/cases/123/unpublish-from-feed/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Or via Admin:**
1. Edit case in admin panel
2. Uncheck ✅ "Is published to feed"
3. Save

---

## 📊 Feed Statistics

Instructors and admins can view feed statistics:

**Endpoint:** `GET /api/cases/feed-statistics/`

**Returns:**
```json
{
  "total_published": 45,
  "department_published": 12,
  "featured_count": 5,
  "total_reactions": 234,
  "by_visibility": {
    "department": 30,
    "university": 15
  },
  "by_specialty": {
    "Nội khoa": 15,
    "Ngoại khoa": 10,
    "Tim mạch": 8
  }
}
```

---

## 🚨 Important Notes

### Permissions:
- ❌ **Students CANNOT publish** cases to feed
- ✅ **Only instructors** can publish/unpublish cases
- ✅ **All authenticated users** can view and react

### Data Model:
- Feed uses **existing Comment model** for reactions
- Comments have `is_reaction=True` flag
- One reaction per user per case (enforced by database)

### Reaction Types:
- `like` - 👍 Thích
- `love` - ❤️ Yêu thích  
- `insightful` - 💡 Hữu ích
- `learned` - 📚 Học được

### Privacy:
- Only **approved** cases can be published
- Instructors control visibility scope
- All reactions are attributed to users

---

## 🔍 Troubleshooting

### "I can't see the Public Feed link"
- Ensure you're logged in
- Check that you're a student or instructor (not admin)
- Refresh the page

### "No cases showing on feed"
- Check if any cases have been published by instructors
- Try changing filter from "Khoa của tôi" to "Tất cả"
- Verify backend is running

### "Can't react to cases"
- Ensure you're logged in
- Check that your JWT token is valid
- Check browser console for errors

### "Permission denied when publishing"
- Only instructors can publish cases
- Verify your role in the system
- Ensure the case is already approved

---

## 📱 Mobile Responsiveness

The feed is fully responsive:
- **Desktop:** Full layout with all features
- **Mobile:** Optimized cards with icon-only reactions
- **Tablet:** Hybrid layout with good readability

---

*Last Updated: November 2025*
