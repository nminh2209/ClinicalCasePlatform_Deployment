# Clinical Case Platform - Complete Setup Guide

## 🚀 Quick Start Guide

This comprehensive guide will help you set up the Clinical Case Platform with medical file attachments, upgraded to Django 5.1+. Choose between standard or test environment setup.

### Prerequisites
- **PostgreSQL** installed and running
- **Node.js** (v18 or higher)
- **Python 3.10+** (required for Django 5.1)
- **Git**
- **Windows OS** (setup scripts are Windows-specific)

## 🎯 Environment Options

### Option A: Test Environment (Recommended for Development)
- Separate database: `clinical_case_platform_test`
- Test settings configuration
- Sample data included
- Isolated from production data

### Option B: Standard Environment
- Standard database configuration
- Production-ready settings
- Manual data setup required

---

## 📊 Setup Method A: Test Environment

### Step 1: Set Up Test Database

1. **Run the PostgreSQL setup script:**
   ```cmd
   setup_postgres_test.bat
   ```

2. **Edit the environment file:**
   - Open `backend\.env.test`
   - Update `DB_PASSWORD=your_actual_postgres_password`

3. **Complete the backend setup:**
   ```cmd
   cd backend
   
   # Install Python dependencies (Django 5.1+)
   pip install -r requirements.txt
   
   # Run migrations with test settings
   python manage.py migrate --settings=clinical_case_platform.settings_test
   
   # Create sample test data
   python manage.py create_test_data --settings=clinical_case_platform.settings_test
   ```

### Step 2: Set Up Frontend

1. **Install frontend dependencies:**
   ```cmd
   cd frontend
   npm install
   ```

2. **Start the frontend development server:**
   ```cmd
   npm run dev
   ```
   📍 Frontend available at: **http://localhost:5173**

### Step 3: Start Backend (Test Environment)

**Method 1: Environment Variable (Recommended)**
```cmd
cd backend
set DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_test
python manage.py runserver
```

**Method 2: Command Flag**
```cmd
cd backend
python manage.py runserver --settings=clinical_case_platform.settings_test
```

**Method 3: PowerShell**
```powershell
cd backend
$env:DJANGO_SETTINGS_MODULE="clinical_case_platform.settings_test"
python manage.py runserver
```

📍 Backend available at: **http://localhost:8000**

---

## 📊 Setup Method B: Standard Environment

### Step 1: Set Up Standard Database

1. **Create PostgreSQL database manually:**
   ```sql
   CREATE DATABASE clinical_case_platform;
   CREATE USER clinical_case_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE clinical_case_platform TO clinical_case_user;
   ```

2. **Configure environment:**
   - Copy `backend\.env.example` to `backend\.env`
   - Update database credentials

3. **Complete the backend setup:**
   ```cmd
   cd backend
   
   # Install Python dependencies (Django 5.1+)
   pip install -r requirements.txt
   
   # Run migrations with standard settings
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

### Step 2: Set Up Frontend
*(Same as Test Environment)*

### Step 3: Start Backend (Standard Environment)

```cmd
cd backend
python manage.py runserver
```

📍 Backend available at: **http://localhost:8000**

## 🧪 Test Accounts (Test Environment Only)

After running the test environment setup, you can use these pre-created accounts:

| Role | Email | Password | Description |
|------|-------|----------|-------------|
| Admin | admin@test.com | testpass123 | Full system access |
| Student 1 | student1@test.com | testpass123 | Student with sample cases |
| Student 2 | student2@test.com | testpass123 | Student account |
| Instructor | instructor1@test.com | testpass123 | Instructor with case management |

## 🌐 Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Vue.js application |
| **Backend API** | http://localhost:8000/api/ | Django REST API |
| **Admin Panel** | http://localhost:8000/admin/ | Django admin interface |
| **API Docs** | http://localhost:8000/api/schema/swagger-ui/ | Interactive API documentation |

## �️ Database Configuration

### Test Environment
- **Database**: `clinical_case_platform_test`
- **Host**: localhost
- **Port**: 5432
- **User**: clinical_case_user
- **Isolated**: Completely separate from production data

### Standard Environment
- **Database**: `clinical_case_platform` (or your choice)
- **Host**: localhost (configurable)
- **Port**: 5432 (configurable)
- **User**: Your PostgreSQL user

## 🔄 Development Workflow

### Daily Development
1. **Start Backend**: 
   - Test env: `python manage.py runserver --settings=clinical_case_platform.settings_test`
   - Standard env: `python manage.py runserver`
2. **Start Frontend**: `npm run dev` (in frontend directory)
3. **Access Application**: Navigate to http://localhost:5173

### Backend Commands Reference

**Test Environment Commands:**
```cmd
# Database migrations
python manage.py migrate --settings=clinical_case_platform.settings_test
python manage.py makemigrations --settings=clinical_case_platform.settings_test

# Data management
python manage.py create_test_data --settings=clinical_case_platform.settings_test
python manage.py shell --settings=clinical_case_platform.settings_test

# Server
python manage.py runserver --settings=clinical_case_platform.settings_test

# Testing
python manage.py test --settings=clinical_case_platform.settings_test
```

**Standard Environment Commands:**
```cmd
# Database migrations
python manage.py migrate
python manage.py makemigrations

# User management
python manage.py createsuperuser
python manage.py shell

# Server
python manage.py runserver

# Testing
python manage.py test
```

## 🏥 Key Features Implemented

### 🩺 Medical File Attachments System
- **16 Vietnamese Medical Categories**:
  - Ảnh chụp chiếu (X-ray Images)
  - Phiếu đo xét nghiệm (Lab Test Results)
  - Ảnh chụp chấn thương (Injury Photos)
  - Ảnh chụp CT scan (CT Scan Images)
  - Ảnh chụp MRI (MRI Images)
  - Ảnh chụp siêu âm (Ultrasound Images)
  - Kết quả điện tim (ECG Results)
  - Kết quả điện não (EEG Results)
  - Phim chụp nội soi (Endoscopy Films)
  - Báo cáo giải phẫu bệnh (Pathology Reports)
  - Hình ảnh y học hạt nhân (Nuclear Medicine Images)
  - Kết quả đo chức năng hô hấp (Respiratory Function Test Results)
  - Ảnh chụp da liễu (Dermatology Photos)
  - Kết quả đo thính lực (Audiometry Results)
  - Kết quả đo thị lực (Vision Test Results)
  - Tài liệu y tế khác (Other Medical Documents)

- **File Management Features**:
  - ✅ Drag-and-drop upload interface
  - ✅ File type validation (images, PDFs, documents)
  - ✅ Confidential file marking
  - ✅ File metadata and descriptions
  - ✅ Secure download with permission checking
  - ✅ Progress indicators during upload
  - ✅ File size limits and validation

### 🖥️ Backend (Django 5.1+):
- ✅ **Upgraded to Django 5.1+** with Python 3.10+ requirement
- ✅ Custom User model with roles (student, instructor, admin)
- ✅ Advanced Clinical Case model with patient data
- ✅ **Medical Attachments System** with Vietnamese categories
- ✅ Case permissions and sharing with confidential file access
- ✅ JWT authentication with refresh tokens
- ✅ CORS configuration for frontend development
- ✅ Separate test database configuration
- ✅ Comprehensive sample test data creation
- ✅ File upload/download API with validation
- ✅ PostgreSQL and SQLite database support

### 🎨 Frontend (Vue.js 3):
- ✅ Vue 3 with Composition API and `<script setup>`
- ✅ Pinia for modern state management
- ✅ Vue Router for SPA navigation
- ✅ Axios for API communication
- ✅ JWT token handling with automatic refresh
- ✅ Authentication store with persistent login
- ✅ Cases management store with medical attachments
- ✅ **Medical File Upload Interface** in case creation
- ✅ **Medical Attachments Display** in case viewing
- ✅ Responsive design with modern UI components
- ✅ Drag-and-drop file upload with progress tracking

### 🔗 API Integration:
- ✅ Comprehensive API service layer
- ✅ Authentication flow with role-based access
- ✅ Case CRUD operations with attachments
- ✅ **Medical file upload/download endpoints**
- ✅ Search and filtering capabilities
- ✅ Error handling and user feedback
- ✅ File validation and security checking

## 🏗️ Project Structure

```
HN2.1ProjectA/
├── backend/                                    # Django 5.1+ Backend
│   ├── clinical_case_platform/
│   │   ├── settings.py                        # Standard configuration
│   │   ├── settings_test.py                   # Test environment configuration
│   │   ├── urls.py                           # Main URL routing
│   │   └── celery.py                         # Background task configuration
│   ├── accounts/                             # User management & authentication
│   │   ├── models.py                         # Custom User model with roles
│   │   ├── serializers.py                    # User API serializers
│   │   ├── views.py                          # Authentication endpoints
│   │   └── urls.py                           # Auth URL routing
│   ├── cases/                                # Clinical case management
│   │   ├── models.py                         # Case & attachment models
│   │   ├── serializers.py                    # Case API serializers
│   │   ├── views.py                          # Case & attachment endpoints
│   │   └── urls.py                           # Case URL routing
│   ├── comments/                             # Case commenting system
│   ├── feedback/                             # Feedback management
│   ├── grades/                               # Grading system
│   ├── exports/                              # Data export functionality
│   ├── repositories/                         # File repository management
│   ├── templates/                            # Template management
│   ├── static/                               # Static files
│   ├── logs/                                 # Application logs
│   ├── requirements.txt                      # Python dependencies (Django 5.1+)
│   ├── .env.test                            # Test environment variables
│   ├── .env.example                         # Environment template
│   ├── README_DETAILED.md                   # Comprehensive backend documentation
│   └── DJANGO_5_UPGRADE.md                  # Django upgrade guide
├── frontend/                                 # Vue.js 3 Frontend
│   ├── src/
│   │   ├── views/
│   │   │   ├── Cases.vue                    # Case listing with medical attachments
│   │   │   ├── CreateCase.vue               # Case creation with file upload
│   │   │   ├── CaseDetail.vue               # Detailed case view
│   │   │   └── Login.vue                    # Authentication interface
│   │   ├── stores/                          # Pinia state management
│   │   │   ├── auth.js                      # Authentication state
│   │   │   └── cases.js                     # Cases & attachments state
│   │   ├── services/                        # API service layer
│   │   │   ├── api.js                       # Base API configuration
│   │   │   ├── auth.js                      # Authentication services
│   │   │   └── cases.js                     # Case & attachment services
│   │   ├── router/                          # Vue Router configuration
│   │   ├── components/                      # Reusable Vue components
│   │   └── assets/                          # Frontend assets
│   ├── package.json                         # Node.js dependencies
│   └── .env.development                     # Frontend environment
├── setup_postgres_test.bat                  # Windows PostgreSQL setup script
├── README_SETUP.md                          # This comprehensive guide
├── VUE_INTEGRATION.md                       # Vue.js integration documentation
├── DomainModel_CRC.md                       # Domain model documentation
└── hmsERDnminh.png                          # Database ERD diagram
```

## 🔗 API Endpoints Reference

### Authentication Endpoints
- `POST /api/auth/login/` - User login with email/password
- `POST /api/auth/logout/` - User logout (invalidate token)
- `POST /api/auth/token/refresh/` - Refresh JWT access token
- `GET /api/auth/user/` - Get current user profile

### Case Management Endpoints
- `GET /api/cases/` - List all accessible cases (with pagination)
- `GET /api/cases/{id}/` - Get specific case details
- `POST /api/cases/` - Create new clinical case
- `PUT /api/cases/{id}/` - Update existing case
- `PATCH /api/cases/{id}/` - Partial case update
- `DELETE /api/cases/{id}/` - Delete case (if authorized)

### Medical Attachments Endpoints
- `GET /api/cases/{case_id}/attachments/` - List case attachments
- `POST /api/cases/{case_id}/attachments/` - Upload medical file
- `GET /api/attachments/{id}/` - Get attachment metadata
- `GET /api/attachments/{id}/download/` - Download attachment file
- `PUT /api/attachments/{id}/` - Update attachment metadata
- `DELETE /api/attachments/{id}/` - Delete attachment (if authorized)

### Additional Endpoints
- `GET /api/cases/{case_id}/comments/` - Get case comments
- `POST /api/cases/{case_id}/comments/` - Add case comment
- `GET /api/users/` - List users (instructors only)
- `GET /api/schema/swagger-ui/` - Interactive API documentation

### Medical Attachment Categories
Each attachment must specify one of these Vietnamese medical categories:
- `xray` - Ảnh chụp chiếu (X-ray Images)
- `lab_test` - Phiếu đo xét nghiệm (Lab Test Results)
- `injury_photo` - Ảnh chụp chấn thương (Injury Photos)
- `ct_scan` - Ảnh chụp CT scan (CT Scan Images)
- `mri` - Ảnh chụp MRI (MRI Images)
- `ultrasound` - Ảnh chụp siêu âm (Ultrasound Images)
- `ecg` - Kết quả điện tim (ECG Results)
- `eeg` - Kết quả điện não (EEG Results)
- `endoscopy` - Phim chụp nội soi (Endoscopy Films)
- `pathology` - Báo cáo giải phẫu bệnh (Pathology Reports)
- `nuclear_medicine` - Hình ảnh y học hạt nhân (Nuclear Medicine Images)
- `respiratory_test` - Kết quả đo chức năng hô hấp (Respiratory Function Test Results)
- `dermatology` - Ảnh chụp da liễu (Dermatology Photos)
- `audiometry` - Kết quả đo thính lực (Audiometry Results)
- `vision_test` - Kết quả đo thị lực (Vision Test Results)
- `other` - Tài liệu y tế khác (Other Medical Documents)

## 🎯 Development Next Steps

### 1. Test the Complete Flow
**Quick Testing Workflow:**
```cmd
# Terminal 1: Start Backend (Test Environment)
cd backend
set DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_test
python manage.py runserver

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

**Testing Checklist:**
- [ ] Login with test accounts (admin@test.com / testpass123)
- [ ] View existing cases with medical attachments
- [ ] Create new case with file uploads
- [ ] Test different medical attachment categories
- [ ] Download and view uploaded files
- [ ] Test user role permissions (student vs instructor)

### 2. Develop New Features
**Frontend Development:**
- Vue 3 components with hot reload enabled
- Pinia stores for state management
- Automatic API proxy to backend (localhost:8000)

**Backend Development:**
- Django 5.1+ with modern features
- REST API with comprehensive serializers
- Database migrations for schema changes
- Test database isolation

### 3. Medical Attachments Workflow
**Upload Process:**
1. Navigate to "Create Case" page
2. Use drag-and-drop interface or click to browse
3. Select medical category from Vietnamese options
4. Add description and mark as confidential if needed
5. Upload with progress tracking

**View Process:**
1. Open any case from the cases list
2. Scroll to "Medical Attachments" section
3. View thumbnails and metadata
4. Download files with permission checking

### 4. Database Management
**Test Environment:**
- Database: `clinical_case_platform_test`
- Completely isolated from production data
- Pre-loaded with sample cases and attachments

**Migration Commands:**
```cmd
# Test environment
python manage.py makemigrations --settings=clinical_case_platform.settings_test
python manage.py migrate --settings=clinical_case_platform.settings_test

# Standard environment  
python manage.py makemigrations
python manage.py migrate
```

## 🚨 Important Notes & Warnings

### ⚠️ Django 5.1+ Requirements
- **Python 3.10+** is REQUIRED (Django 5.1 dropped Python 3.9 support)
- Check your Python version: `python --version`
- Upgrade Python if needed before installation

### 🔒 Security Considerations
- **File Upload Security**: All uploads are validated for file type and size
- **Confidential Files**: Marked files require special permissions to access
- **JWT Tokens**: Automatically refresh to maintain secure sessions
- **CORS Configuration**: Properly configured for frontend development

### 🗃️ Database Isolation
- **Test Environment**: Uses `clinical_case_platform_test` database
- **No Data Conflicts**: Your original data remains completely untouched
- **Environment Variables**: Different `.env` files for different environments
- **Migration Safety**: Test migrations run independently

### 📁 File Storage
- **Upload Directory**: `backend/media/case_attachments/`
- **File Permissions**: Automatically set based on confidentiality settings
- **Backup Strategy**: Consider backing up the media directory for production

### 🌐 Development Ports
- **Frontend**: http://localhost:5173 (Vite development server)
- **Backend**: http://localhost:8000 (Django development server)
- **Database**: localhost:5432 (PostgreSQL default)
- **Conflicts**: Ensure no other services are using these ports

## 🐛 Troubleshooting Guide

### Python/Django Issues

**Python Version Error:**
```
ERROR: Django 5.1 requires Python 3.10 or higher
```
**Solution:** Upgrade to Python 3.10+ and reinstall dependencies

**Database Connection Issues:**
```
django.db.utils.OperationalError: FATAL: password authentication failed
```
**Solutions:**
1. Check PostgreSQL is running: `pg_ctl status`
2. Verify credentials in `.env` or `.env.test`
3. Test connection: `psql -U clinical_case_user -d clinical_case_platform_test`

**Migration Issues:**
```
django.db.utils.ProgrammingError: relation "accounts_user" does not exist
```
**Solution:** Run migrations with correct settings:
```cmd
python manage.py migrate --settings=clinical_case_platform.settings_test
```

### Frontend Issues

**Node.js Compatibility:**
```
ERROR: Node.js version 16.x.x is not supported
```
**Solution:** Upgrade to Node.js 18+ for Vue 3 compatibility

**API Connection Issues:**
```
Network Error: Request failed with status code 500
```
**Solutions:**
1. Verify backend is running on http://localhost:8000
2. Check CORS configuration in Django settings
3. Verify API endpoints in browser network tab

**File Upload Issues:**
```
413 Request Entity Too Large
```
**Solution:** Check Django `FILE_UPLOAD_MAX_MEMORY_SIZE` and `DATA_UPLOAD_MAX_MEMORY_SIZE` settings

### Database Issues

**PostgreSQL Service Issues:**
```
ERROR: could not connect to server
```
**Solutions:**
1. Windows: `net start postgresql-x64-14`
2. Check PostgreSQL service in Task Manager
3. Verify PostgreSQL installation

**Permission Issues:**
```
FATAL: role "clinical_case_user" does not exist
```
**Solution:** Re-run the setup script: `setup_postgres_test.bat`

### File Upload Issues

**File Not Found Errors:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'media/case_attachments/'
```
**Solution:** Create media directories:
```cmd
cd backend
mkdir media
mkdir media\case_attachments
```

**File Permission Issues:**
```
PermissionError: [Errno 13] Permission denied
```
**Solution:** Check file permissions and run as administrator if needed

### Environment Configuration

**Settings Module Issues:**
```
ImportError: No module named 'clinical_case_platform.settings_test'
```
**Solution:** Ensure you're in the correct directory and settings file exists

**Environment Variables:**
```
KeyError: 'SECRET_KEY'
```
**Solution:** Copy `.env.example` to `.env` and configure all required variables

## � Additional Documentation

### Comprehensive Guides
- **`backend/README_DETAILED.md`** - Complete backend setup and API documentation
- **`backend/DJANGO_5_UPGRADE.md`** - Django 5.1 upgrade guide and compatibility notes
- **`VUE_INTEGRATION.md`** - Vue.js integration and frontend architecture
- **`DomainModel_CRC.md`** - Domain model and system architecture

### Quick Reference Commands

**Test Environment Setup:**
```cmd
# Full setup from scratch
setup_postgres_test.bat
cd backend
pip install -r requirements.txt
python manage.py migrate --settings=clinical_case_platform.settings_test
python manage.py create_test_data --settings=clinical_case_platform.settings_test

# Start development servers
set DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_test
python manage.py runserver

# In another terminal
cd frontend
npm install
npm run dev
```

**Standard Environment Setup:**
```cmd
# Database setup (manual)
createdb clinical_case_platform
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Start development servers
python manage.py runserver

# In another terminal
cd frontend
npm install
npm run dev
```

## 📞 Support & Resources

### Getting Help
1. **Check Documentation**: Start with `README_DETAILED.md` for comprehensive guides
2. **Console Output**: Always check terminal/console for error messages
3. **Network Tab**: Use browser developer tools to debug API calls
4. **Log Files**: Check `backend/logs/django.log` for detailed error logs

### Development Resources
- **Django 5.1 Documentation**: https://docs.djangoproject.com/en/5.1/
- **Vue 3 Documentation**: https://vuejs.org/guide/
- **Pinia State Management**: https://pinia.vuejs.org/
- **Django REST Framework**: https://www.django-rest-framework.org/

### Medical Terminology Reference
The system uses Vietnamese medical terminology for file categories. Each category has both Vietnamese display names and English identifiers for API usage.

---

## 🎉 Success! Your Clinical Case Platform is Ready

Your comprehensive medical case management platform with file attachments is now fully configured and ready for development. The system includes:

✅ **Django 5.1+ Backend** with modern Python features  
✅ **Vue 3 Frontend** with composition API and modern tooling  
✅ **Medical File Attachments** with 16 Vietnamese categories  
✅ **Secure Authentication** with JWT and role-based access  
✅ **Database Isolation** for safe development  
✅ **Comprehensive Documentation** for all scenarios  

**Quick Start**: Run the test environment setup and navigate to http://localhost:5173 to begin!

---

*Last Updated: October 2025 - Django 5.1+ Compatible*