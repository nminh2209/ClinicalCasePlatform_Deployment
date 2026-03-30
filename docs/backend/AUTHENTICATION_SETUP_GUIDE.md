# Authentication System Setup Guide

## Overview

The Clinical Case Platform now includes:
1. **User Registration** - Public self-registration for students/instructors
2. **Forgot Password** - Email-based password reset flow
3. **Social Login** - Google and Microsoft OAuth authentication

---

## Features Implemented

### 1. User Registration (`/register`)
- Full registration form with role selection (student/instructor)
- Client-side and server-side validation
- Automatic login after registration
- Conditional fields (student ID for students, employee ID for instructors)
- Password strength requirements (8+ chars, mixed case, numbers)

### 2. Forgot Password Flow
- **Request Reset** (`/forgot-password`): Email input form
- **Reset Password** (`/reset-password/:uid/:token`): New password form with token validation
- Email with reset link sent to user
- 24-hour token expiration
- Security: Doesn't reveal if email exists

### 3. Social Authentication
- **Google OAuth**: One-click login with Google account
- **Microsoft OAuth**: One-click login with Microsoft/school account
- Auto-creates user on first login
- Uses OAuth 2.0 implicit flow
- Returns JWT tokens for API access

---

## Frontend Files Created

### New Components
- **`frontend/src/views/Register.vue`** (578 lines)
  - Registration form with role-based fields
  - Password confirmation validation
  - Success message with auto-redirect

- **`frontend/src/views/ForgotPassword.vue`** (289 lines)
  - Email input form
  - Success state with instructions

- **`frontend/src/views/ResetPassword.vue`** (615 lines)
  - New password form with confirmation
  - Token validation from URL params
  - Success state with auto-redirect to login

- **`frontend/src/views/OAuthCallback.vue`** (161 lines)
  - Handles OAuth redirects (Google + Microsoft)
  - Exchanges access token for JWT
  - Auto-login and redirect to home

### Updated Components
- **`frontend/src/views/Login.vue`** (Modified)
  - Added "Quên mật khẩu?" link
  - Added Google login button
  - Added Microsoft login button
  - Added "Đăng ký ngay" link
  - Social login handlers with OAuth redirects

- **`frontend/src/main.ts`** (Modified)
  - Route: `/register` → Register.vue
  - Route: `/forgot-password` → ForgotPassword.vue
  - Route: `/reset-password/:uid/:token` → ResetPassword.vue
  - Route: `/auth/google/callback` → OAuthCallback.vue
  - Route: `/auth/microsoft/callback` → OAuthCallback.vue

---

## Backend Files Modified

### Serializers (`backend/accounts/serializers.py`)
**Added:**
- `PasswordResetRequestSerializer` - Validates email, sends reset email
- `PasswordResetConfirmSerializer` - Validates token, resets password

**Imports:**
- `default_token_generator` - Django's secure token generator
- `urlsafe_base64_encode/decode` - Encode user ID in URL
- `send_mail` - Send password reset emails

### Views (`backend/accounts/views.py`)
**Added:**
- `PasswordResetRequestView` - POST `/api/auth/password-reset/`
  - Validates email
  - Generates reset token
  - Sends email with reset link

- `PasswordResetConfirmView` - POST `/api/auth/password-reset-confirm/`
  - Validates uid and token
  - Updates user password

- `GoogleLoginView` - POST `/api/auth/google/`
  - Verifies Google access token
  - Creates or retrieves user
  - Returns JWT tokens

- `MicrosoftLoginView` - POST `/api/auth/microsoft/`
  - Verifies Microsoft access token via Graph API
  - Creates or retrieves user
  - Returns JWT tokens

### URLs (`backend/accounts/urls.py`)
**Added routes:**
```python
path("password-reset/", PasswordResetRequestView.as_view())
path("password-reset-confirm/", PasswordResetConfirmView.as_view())
path("google/", GoogleLoginView.as_view())
path("microsoft/", MicrosoftLoginView.as_view())
```

### Settings (`backend/clinical_case_platform/settings.py`)
**Added:**
```python
DEFAULT_FROM_EMAIL = "noreply@clinicalcase.edu"
FRONTEND_URL = "http://localhost:5173"
```

---

## Configuration Required

### 1. Email Settings (Password Reset)

**Option A: Console Backend (Development)**
Already configured in settings.py:
```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```
Emails will print in the terminal instead of sending.

**Option B: Gmail SMTP (Production)**
Create `.env` file in `backend/` directory:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@clinicalcase.edu
FRONTEND_URL=http://localhost:5173
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `EMAIL_HOST_PASSWORD`

---

### 2. Google OAuth Setup

**Step 1: Create Google OAuth Client**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable "Google+ API"
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Authorized JavaScript origins:
   - `http://localhost:5173`
   - `http://localhost:8000`
7. Authorized redirect URIs:
   - `http://localhost:5173/auth/google/callback`
8. Copy **Client ID**

**Step 2: Configure Frontend**
Create `frontend/.env` file:
```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
```

**Test:**
```bash
cd frontend
npm run dev
# Open http://localhost:5173/login
# Click "Đăng nhập với Google"
```

---

### 3. Microsoft OAuth Setup

**Step 1: Register Application in Azure AD**
1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Name: "Clinical Case Platform"
5. Supported account types: **Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts**
6. Redirect URI:
   - Platform: **Single-page application (SPA)**
   - URI: `http://localhost:5173/auth/microsoft/callback`
7. Click **Register**
8. Copy **Application (client) ID**

**Step 2: Configure API Permissions**
1. Go to **API permissions** → **Add a permission**
2. Select **Microsoft Graph**
3. Select **Delegated permissions**
4. Add: `User.Read`, `email`, `openid`, `profile`
5. Click **Grant admin consent** (if available)

**Step 3: Configure Frontend**
Add to `frontend/.env`:
```env
VITE_MICROSOFT_CLIENT_ID=your-microsoft-client-id-here
```

**Test:**
```bash
cd frontend
npm run dev
# Open http://localhost:5173/login
# Click "Đăng nhập với Microsoft"
```

---

## Testing Flows

### 1. Registration Flow
```bash
# Frontend
cd frontend
npm run dev

# Backend
cd backend
python manage.py runserver
```

**Test steps:**
1. Go to http://localhost:5173/login
2. Click "Đăng ký ngay"
3. Fill form:
   - Email: test@example.com
   - Username: testuser
   - First Name: Nguyễn
   - Last Name: Văn A
   - Role: Sinh viên
   - Student ID: SV2024999
   - Password: TestPass123
   - Confirm Password: TestPass123
4. Click "Đăng ký"
5. Should redirect to login after 2 seconds
6. Login with new credentials

### 2. Forgot Password Flow

**Test steps:**
1. Go to http://localhost:5173/login
2. Click "Quên mật khẩu?"
3. Enter email: admin@test.com
4. Click "Gửi hướng dẫn đặt lại mật khẩu"
5. Check backend terminal for reset link (if using console backend)
6. Copy URL like: `http://localhost:5173/reset-password/Mg/abc123-xyz/`
7. Paste in browser
8. Enter new password (2 times)
9. Click "Đặt lại mật khẩu"
10. Should redirect to login
11. Login with new password

### 3. Google Login Flow

**Prerequisites:**
- Configure Google OAuth (see above)
- Add `VITE_GOOGLE_CLIENT_ID` to frontend/.env

**Test steps:**
1. Go to http://localhost:5173/login
2. Click "Đăng nhập với Google"
3. Redirects to Google login
4. Select Google account
5. Grant permissions
6. Redirects back to app
7. Logs in automatically
8. Redirects to /home

**First-time user:**
- Creates account with:
  - Email: from Google
  - Username: email prefix (before @)
  - First Name: from Google
  - Last Name: from Google
  - Role: "student" (default)
  - Password: unusable (OAuth only)

### 4. Microsoft Login Flow

**Prerequisites:**
- Configure Microsoft OAuth (see above)
- Add `VITE_MICROSOFT_CLIENT_ID` to frontend/.env

**Test steps:**
1. Go to http://localhost:5173/login
2. Click "Đăng nhập với Microsoft"
3. Redirects to Microsoft login
4. Enter Microsoft/school credentials
5. Grant permissions
6. Redirects back to app
7. Logs in automatically
8. Redirects to /home

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login with email/password |
| POST | `/api/auth/logout/` | Logout (blacklist refresh token) |
| POST | `/api/auth/token/refresh/` | Refresh access token |

### Password Reset
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/password-reset/` | Request password reset email |
| POST | `/api/auth/password-reset-confirm/` | Confirm reset with token |

### Social Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/google/` | Exchange Google token for JWT |
| POST | `/api/auth/microsoft/` | Exchange Microsoft token for JWT |

---

## Security Considerations

### Password Reset
- Tokens expire after 24 hours
- One-time use tokens (Django's `default_token_generator`)
- Doesn't reveal if email exists
- Uses secure URL encoding (base64)
- Requires both uid and token to reset

### Social Auth
- Verifies tokens with provider APIs:
  - Google: `https://www.googleapis.com/oauth2/v3/userinfo`
  - Microsoft: `https://graph.microsoft.com/v1.0/me`
- Creates users with unusable passwords (OAuth only)
- JWT tokens for subsequent API calls
- No credentials stored on backend

### General
- Password validation: 8+ chars, mixed case, numbers
- JWT tokens with refresh mechanism
- CORS configured for frontend origin
- HTTPS required in production

---

## Production Deployment

### Frontend Environment Variables
```env
VITE_GOOGLE_CLIENT_ID=production-google-client-id
VITE_MICROSOFT_CLIENT_ID=production-microsoft-client-id
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Backend Environment Variables
```env
# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-production-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Frontend URL
FRONTEND_URL=https://yourdomain.com

# Django
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com
```

### Update OAuth Redirect URIs
**Google:**
- Add `https://yourdomain.com/auth/google/callback`

**Microsoft:**
- Add `https://yourdomain.com/auth/microsoft/callback`

### HTTPS Requirements
- Both Google and Microsoft require HTTPS in production
- Use Let's Encrypt or cloud provider certificates
- Update `SECURE_SSL_REDIRECT = True` in settings.py

---

## Troubleshooting

### Email Not Sending
**Problem:** Password reset emails not arriving

**Solution:**
1. Check `EMAIL_BACKEND` in settings or .env
2. For Gmail, ensure app password is correct
3. Check spam folder
4. Use console backend for testing: `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

### Google Login Error
**Problem:** "redirect_uri_mismatch"

**Solution:**
1. Check authorized redirect URIs in Google Console
2. Must exactly match: `http://localhost:5173/auth/google/callback`
3. No trailing slash mismatches
4. Check both HTTP and HTTPS

### Microsoft Login Error
**Problem:** "AADSTS50011: The reply URL specified in the request does not match"

**Solution:**
1. Check redirect URI in Azure AD
2. Platform must be "Single-page application (SPA)"
3. Must exactly match: `http://localhost:5173/auth/microsoft/callback`

### Token Expired Error
**Problem:** "Invalid or expired reset link"

**Solution:**
- Reset tokens expire after 24 hours
- Request new password reset email
- Check system time is correct

---

## Future Enhancements

### Planned Features
1. **Email Verification** - Require email confirmation on registration
2. **Two-Factor Authentication** - SMS or authenticator app
3. **Account Linking** - Link Google/Microsoft to existing accounts
4. **Role Upgrade Requests** - Students request instructor role
5. **Admin Approval** - Manual approval for new registrations

### Additional OAuth Providers
- GitHub (for developers)
- Facebook
- Apple ID
- University SSO systems

---

## Support

If you encounter issues:
1. Check backend terminal logs
2. Check browser console for errors
3. Verify environment variables are set
4. Test with curl or Postman
5. Check OAuth provider dashboards

For password reset emails, temporarily use console backend to see the reset links in terminal output.
