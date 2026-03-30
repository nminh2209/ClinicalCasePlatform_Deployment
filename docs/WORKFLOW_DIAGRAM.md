# Clinical Case Management Platform - Workflow Diagrams

## 1. Overall System Workflow

```mermaid
flowchart TD
    A[User Access] --> B{Authentication}
    B -->|Login Success| C[Dashboard]
    B -->|Login Failed| A
    B -->|New User| D[Register]
    B -->|Forgot Password| E[Password Reset]
    B -->|Social Login| F[OAuth Flow]

    D --> G[Fill Registration Form]
    G --> H[Select Role]
    H --> C

    E --> I[Enter Email]
    I --> J[Receive Reset Link]
    J --> K[Set New Password]
    K --> A

    F --> L{Provider}
    L -->|Google| M[Google OAuth]
    L -->|Microsoft| N[Microsoft OAuth]
    M --> O[Verify Token]
    N --> O
    O --> P[Create/Login User]
    P --> C

    C --> Q{User Role}
    Q -->|Student| R[Student Workflow]
    Q -->|Instructor| S[Instructor Workflow]
    Q -->|Admin| T[Admin Workflow]

    R --> U[Create Cases]
    R --> V[Browse Cases]
    R --> W[Upload Medical Files]
    R --> X[Export Cases]

    S --> Y[Review Cases]
    S --> Z[Grade Cases]
    S --> AA[Give Feedback]
    S --> AB[Manage Templates]

    T --> AC[Manage Users]
    T --> AD[System Configuration]
    T --> AE[Department Management]

    U --> AF[Case Repository]
    V --> AF
    Y --> AF

    AF --> AG[Search & Filter]
    AF --> AH[Case Details]
    AF --> AI[Collaboration]

    AH --> AJ[Medical Attachments]
    AH --> AK[Comments]
    AH --> AL[Feedback]

    X --> AM[Export Formats]
    AM --> AN[PDF]
    AM --> AO[Word]
    AM --> AP[PowerPoint]
```

## 1A. Authentication Workflow

```mermaid
flowchart TD
    A[Landing Page] --> B{Choose Action}
    
    B -->|Login| C[Login Form]
    B -->|Register| D[Registration Form]
    B -->|Forgot Password| E[Password Reset Request]
    
    C --> F[Enter Email & Password]
    F --> G{Valid Credentials?}
    G -->|Yes| H[Receive JWT Tokens]
    G -->|No| I[Show Error Message]
    I --> C
    
    C --> J[Click Social Login]
    J --> K{Provider}
    K -->|Google| L[Redirect to Google OAuth]
    K -->|Microsoft| M[Redirect to Microsoft OAuth]
    
    L --> N[User Authorizes App]
    M --> N
    N --> O[Redirect with Access Token]
    O --> P[Backend Verifies Token]
    P --> Q{Valid Token?}
    Q -->|Yes| R[Get/Create User]
    Q -->|No| S[Show Error]
    S --> C
    R --> H
    
    H --> T[Store Tokens in Local Storage]
    T --> U[Redirect to Dashboard]
    
    D --> V[Fill Registration Form]
    V --> W[Enter Email, Username, Password]
    W --> X[Select Role]
    X --> Y{Role-Specific Fields}
    Y -->|Student| Z[Enter Student ID]
    Y -->|Instructor| AA[Enter Employee ID]
    Y -->|Admin| AB[Admin Fields]
    Z --> AC[Submit Registration]
    AA --> AC
    AB --> AC
    AC --> AD{Valid Data?}
    AD -->|Yes| AE[Create User Account]
    AD -->|No| AF[Show Validation Errors]
    AF --> D
    AE --> H
    
    E --> AG[Enter Email Address]
    AG --> AH[Submit Reset Request]
    AH --> AI[Backend Generates Token]
    AI --> AJ[Send Email with Reset Link]
    AJ --> AK[User Clicks Email Link]
    AK --> AL[Redirect to Reset Password Page]
    AL --> AM[Enter New Password]
    AM --> AN[Submit with Token & UID]
    AN --> AO{Valid Token?}
    AO -->|Yes| AP[Update Password]
    AO -->|No| AQ[Show Token Expired Error]
    AQ --> E
    AP --> AR[Show Success Message]
    AR --> AS[Auto-Redirect to Login]
    AS --> C
```

## 1B. OAuth Social Login Detailed Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Google/Microsoft
    participant Backend
    participant Database

    User->>Frontend: Click "Login with Google/Microsoft"
    Frontend->>Frontend: Redirect to OAuth Provider
    Frontend->>Google/Microsoft: Authorization Request
    Note over Frontend,Google/Microsoft: redirect_uri=/auth/{provider}/callback
    Google/Microsoft->>User: Show Login Page
    User->>Google/Microsoft: Enter Credentials & Authorize
    Google/Microsoft->>Frontend: Redirect with access_token
    Frontend->>Frontend: Extract token from URL hash
    Frontend->>Backend: POST /api/auth/{provider}/ with access_token
    Backend->>Google/Microsoft: Verify Token
    Google/Microsoft->>Backend: Return User Info (email, name)
    Backend->>Database: Check if user exists
    alt User Exists
        Database->>Backend: Return User
    else New User
        Backend->>Database: Create New User
        Note over Backend,Database: Set unusable password<br/>OAuth-only account
        Database->>Backend: Return New User
    end
    Backend->>Backend: Generate JWT Tokens
    Backend->>Frontend: Return {user, tokens, is_new_user}
    Frontend->>Frontend: Store tokens in localStorage
    Frontend->>Frontend: Update auth store
    Frontend->>User: Redirect to /home
```

## 1C. Password Reset Token Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Email
    participant TokenGenerator

    User->>Frontend: Enter email at /forgot-password
    Frontend->>Backend: POST /api/auth/password-reset/
    Backend->>Backend: Check if user exists
    alt User Exists
        Backend->>TokenGenerator: Generate reset token
        TokenGenerator->>Backend: Return token & uid (base64)
        Backend->>Email: Send reset link
        Note over Backend,Email: Link: /reset-password/{uid}/{token}
        Email->>User: Reset email delivered
    end
    Backend->>Frontend: "Reset link sent" (always)
    Note over Backend,Frontend: No indication if email exists (security)
    
    User->>Email: Click reset link
    Email->>Frontend: Open /reset-password/{uid}/{token}
    Frontend->>Frontend: Display reset form
    User->>Frontend: Enter new password + confirm
    Frontend->>Backend: POST /api/auth/password-reset-confirm/
    Backend->>Backend: Decode uid (base64)
    Backend->>TokenGenerator: Validate token
    alt Token Valid & Not Expired
        TokenGenerator->>Backend: Token valid
        Backend->>Backend: Update user password
        Backend->>Backend: Mark token as used
        Backend->>Frontend: "Password reset successful"
        Frontend->>Frontend: Show success message
        Frontend->>Frontend: Auto-redirect to /login (3s)
    else Token Invalid/Expired
        TokenGenerator->>Backend: Token invalid
        Backend->>Frontend: "Token expired or invalid"
        Frontend->>User: Show error message
    end
```

## 2. Student Case Creation Workflow

```mermaid
flowchart TD
    A[Student Login] --> B[Navigate to Cases]
    B --> C[Click 'Tạo hồ sơ mới']
    C --> D[Select Case Template]
    D --> E{Template Type}

    E -->|Cardiology| F[Tim mạch Template]
    E -->|Internal Medicine| G[Nội khoa Template]
    E -->|Surgery| H[Phẫu thuật Template]
    E -->|Respiratory| I[Hô hấp Template]

    F --> J[Fill Patient Information]
    G --> J
    H --> J
    I --> J

    J --> K[Clinical History Section]
    K --> L[Physical Examination]
    L --> M[Investigations]
    M --> N[Diagnosis & Management]
    N --> O[Learning Outcomes]

    O --> P[Upload Medical Attachments]
    P --> Q{Attachment Type}

    Q -->|X-ray| R[Ảnh chụp X-quang]
    Q -->|Lab Results| S[Kết quả xét nghiệm]
    Q -->|CT Scan| T[Ảnh chụp CT]
    Q -->|ECG| U[Kết quả điện tim]
    Q -->|Photos| V[Ảnh chụp tổn thương]

    R --> W[Add Metadata & Notes]
    S --> W
    T --> W
    U --> W
    V --> W

    W --> X[Set Confidentiality Level]
    X --> Y[Save as Draft]
    Y --> Z{Ready to Submit?}

    Z -->|No| AA[Continue Editing]
    Z -->|Yes| BB[Submit for Review]

    AA --> J
    BB --> CC[Case in Repository]
    CC --> DD[Notification to Instructor]
```

## 3. Medical File Upload Workflow

```mermaid
flowchart TD
    A[Access Case Editor] --> B[Medical Attachments Section]
    B --> C[Click 'Thêm tệp y tế']
    C --> D[Drag & Drop Interface]

    D --> E{File Selection}
    E -->|Single File| F[Select File]
    E -->|Multiple Files| G[Select Multiple]

    F --> H[File Validation]
    G --> H

    H --> I{File Valid?}
    I -->|No| J[Show Error Message]
    I -->|Yes| K[Choose Category]

    J --> D

    K --> L{Vietnamese Categories}
    L -->|Ảnh chụp X-quang| M[X-ray Images]
    L -->|Kết quả xét nghiệm máu| N[Blood Test Results]
    L -->|Ảnh chụp CT scan| O[CT Scan Images]
    L -->|Kết quả điện tim| P[ECG Results]
    L -->|Ảnh chụp MRI| Q[MRI Images]
    L -->|Kết quả siêu âm| R[Ultrasound Results]
    L -->|Ảnh chụp tổn thương| S[Injury Photos]
    L -->|Đơn thuốc| T[Prescription]
    L -->|Kết quả nội soi| U[Endoscopy Results]
    L -->|Ảnh chụp vi khuẩn học| V[Microbiology Images]
    L -->|Kết quả giải phẫu bệnh| W[Pathology Results]
    L -->|Biểu đồ theo dõi| X[Monitoring Charts]
    L -->|Báo cáo phẫu thuật| Y[Surgery Reports]
    L -->|Kế hoạch điều trị| Z[Treatment Plans]
    L -->|Ghi chú xuất viện| AA[Discharge Notes]
    L -->|Khác| BB[Other Files]

    M --> CC[Add File Metadata]
    N --> CC
    O --> CC
    P --> CC
    Q --> CC
    R --> CC
    S --> CC
    T --> CC
    U --> CC
    V --> CC
    W --> CC
    X --> CC
    Y --> CC
    Z --> CC
    AA --> CC
    BB --> CC

    CC --> DD[Enter Title & Description]
    DD --> EE[Set Date Taken]
    EE --> FF[Add Physician Notes]
    FF --> GG[Set Confidentiality]

    GG --> HH{Confidential?}
    HH -->|Yes| II[Instructor Only Access]
    HH -->|No| JJ[Student & Instructor Access]

    II --> KK[Upload Progress]
    JJ --> KK

    KK --> LL[File Processing]
    LL --> MM[Generate Thumbnail]
    MM --> NN[Save to Database]
    NN --> OO[Update Case]
    OO --> PP[Success Notification]
```

## 4. Instructor Review & Grading Workflow

```mermaid
flowchart TD
    A[Instructor Login] --> B[Dashboard Overview]
    B --> C[View Pending Cases]
    C --> D[Filter by Department/Specialty]
    D --> E[Select Case to Review]

    E --> F[Case Overview]
    F --> G[Review Patient Information]
    G --> H[Evaluate Clinical Sections]

    H --> I[Check Clinical History]
    I --> J[Review Physical Examination]
    J --> K[Assess Investigations]
    K --> L[Evaluate Diagnosis & Management]
    L --> M[Review Learning Outcomes]

    M --> N[Examine Medical Attachments]
    N --> O{Medical Files Present?}
    O -->|Yes| P[Review Each Attachment]
    O -->|No| Q[Note Missing Files]

    P --> R[Validate File Relevance]
    R --> S[Check File Quality]
    S --> T[Verify Medical Accuracy]

    T --> U[Provide Feedback]
    Q --> U

    U --> V[Clinical Reasoning Feedback]
    V --> W[Documentation Quality Feedback]
    W --> X[Medical File Assessment]
    X --> Y[Learning Objectives Evaluation]

    Y --> Z[Assign Grades]
    Z --> AA[Overall Score]
    AA --> BB[Clinical Reasoning Score]
    BB --> CC[Documentation Score]
    CC --> DD[Medical Files Score]

    DD --> EE[Add Evaluation Notes]
    EE --> FF{Case Status}
    FF -->|Needs Revision| GG[Request Changes]
    FF -->|Approved| HH[Mark as Reviewed]
    FF -->|Excellent| II[Mark as Exemplar]

    GG --> JJ[Send Feedback to Student]
    HH --> JJ
    II --> JJ

    JJ --> KK[Update Case Status]
    KK --> LL[Notify Student]
    LL --> MM[Add to Grade Book]
```

## 5. Collaborative Learning Workflow

```mermaid
flowchart TD
    A[Student with Case] --> B[Share Case]
    B --> C[Set Permissions]
    C --> D{Permission Type}

    D -->|View Only| E[Read Access]
    D -->|Comment| F[View + Comment]
    D -->|Edit| G[Full Access]

    E --> H[Share with Classmates]
    F --> H
    G --> H

    H --> I[Send Invitations]
    I --> J[Classmates Receive Notification]
    J --> K[Accept Invitation]

    K --> L[Access Shared Case]
    L --> M{User Action}

    M -->|View| N[Read Case Details]
    M -->|Comment| O[Add Discussion Comments]
    M -->|Edit| P[Contribute to Case]

    N --> Q[Learn from Case]
    O --> R[Discussion Thread]
    P --> S[Collaborative Editing]

    R --> T[Reply to Comments]
    T --> U[Peer Learning Discussion]

    S --> V[Track Changes]
    V --> W[Version History]
    W --> X[Merge Contributions]

    U --> Y[Group Learning Outcomes]
    X --> Y
    Q --> Y

    Y --> Z[Export Collaborative Case]
    Z --> AA[Individual Learning Portfolio]
```

## 6. Case Export & Presentation Workflow

```mermaid
flowchart TD
    A[Select Case] --> B[Choose Export Format]
    B --> C{Export Type}

    C -->|PDF| D[Academic Report Format]
    C -->|Word| E[Editable Document]
    C -->|PowerPoint| F[Presentation Format]

    D --> G[Include Medical Images]
    E --> G
    F --> G

    G --> H{Include Confidential Files?}
    H -->|Yes| I[Check User Permissions]
    H -->|No| J[Skip Confidential Files]

    I --> K{Has Permission?}
    K -->|Yes| L[Include All Files]
    K -->|No| M[Exclude Confidential]

    J --> N[Generate Export]
    L --> N
    M --> N

    N --> O[Format Content]
    O --> P{Export Format}

    P -->|PDF| Q[Vietnamese Medical Report Layout]
    P -->|Word| R[Structured Document Template]
    P -->|PowerPoint| S[Clinical Case Slides]

    Q --> T[Embed Medical Images]
    R --> T
    S --> T

    T --> U[Add Case Metadata]
    U --> V[Include Student Information]
    V --> W[Add Export Timestamp]
    W --> X[Generate File]

    X --> Y[Save to Downloads]
    Y --> Z[Success Notification]
    Z --> AA[File Ready for Use]

    AA --> BB{Usage Purpose}
    BB -->|Academic| CC[Submit Assignment]
    BB -->|Research| DD[Research Documentation]
    BB -->|Presentation| EE[Clinical Rounds]
    BB -->|Portfolio| FF[Learning Portfolio]
```

## 7. System Authentication & Session Management

```mermaid
flowchart TD
    A[User Access] --> B[Login Page]
    B --> C[Enter Credentials]
    C --> D[Submit Login Form]

    D --> E[Backend Validation]
    E --> F{Credentials Valid?}

    F -->|No| G[Show Error Message]
    F -->|Yes| H[Generate JWT Tokens]

    G --> B

    H --> I[Access Token + Refresh Token]
    I --> J[Store Tokens in Frontend]
    J --> K[Set User Session]
    K --> L[Redirect to Dashboard]

    L --> M[Protected Route Access]
    M --> N{Token Valid?}

    N -->|Yes| O[Allow Access]
    N -->|Expired| P[Use Refresh Token]
    N -->|Invalid| Q[Redirect to Login]

    P --> R{Refresh Valid?}
    R -->|Yes| S[Generate New Access Token]
    R -->|No| Q

    S --> T[Update Frontend Storage]
    T --> O

    O --> U[User Activity]
    U --> V{Session Active?}

    V -->|Yes| W[Continue Session]
    V -->|Timeout| X[Auto Logout]

    W --> U
    X --> Y[Clear Session Data]
    Y --> Q

    Q --> Z[Login Required]
    Z --> B
```

## 8. Database & API Interaction Flow

```mermaid
flowchart TD
    A[Frontend Action] --> B[Pinia Store]
    B --> C[Service Layer]
    C --> D[API Call]

    D --> E{HTTP Method}
    E -->|GET| F[Retrieve Data]
    E -->|POST| G[Create Data]
    E -->|PUT| H[Update Data]
    E -->|DELETE| I[Delete Data]

    F --> J[Django REST API]
    G --> J
    H --> J
    I --> J

    J --> K[Authentication Check]
    K --> L{JWT Valid?}

    L -->|No| M[401 Unauthorized]
    L -->|Yes| N[Permission Check]

    M --> O[Redirect to Login]

    N --> P{Has Permission?}
    P -->|No| Q[403 Forbidden]
    P -->|Yes| R[Process Request]

    Q --> S[Error Response]

    R --> T[Database Query]
    T --> U[PostgreSQL Database]
    U --> V[Execute Query]
    V --> W[Return Results]

    W --> X[Serialize Data]
    X --> Y[JSON Response]
    Y --> Z[Send to Frontend]

    Z --> AA[Update Store State]
    AA --> BB[Reactive UI Update]
    BB --> CC[User Sees Changes]

    S --> DD[Error Handling]
    O --> DD
    DD --> EE[Display Error Message]
```

This comprehensive workflow documentation covers all major user interactions and system processes in your Vietnamese Clinical Case Management Platform. Each diagram shows the complete flow from user action to system response, making it easy to understand how the platform operates.
