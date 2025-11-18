# Clinical Case Management Platform - Workflow Diagrams

## 1. Overall System Workflow

```mermaid
flowchart TD
    A[User Access] --> B{Authentication}
    B -->|Login Success| C[Dashboard]
    B -->|Login Failed| A
    
    C --> D{User Role}
    D -->|Student| E[Student Workflow]
    D -->|Instructor| F[Instructor Workflow]
    D -->|Admin| G[Admin Workflow]
    
    E --> H[Create Cases]
    E --> I[Browse Cases]
    E --> J[Upload Medical Files]
    E --> K[Export Cases]
    
    F --> L[Review Cases]
    F --> M[Grade Cases]
    F --> N[Give Feedback]
    F --> O[Manage Templates]
    
    G --> P[Manage Users]
    G --> Q[System Configuration]
    G --> R[Department Management]
    
    H --> S[Case Repository]
    I --> S
    L --> S
    
    S --> T[Search & Filter]
    S --> U[Case Details]
    S --> V[Collaboration]
    
    U --> W[Medical Attachments]
    U --> X[Comments]
    U --> Y[Feedback]
    
    K --> Z[Export Formats]
    Z --> AA[PDF]
    Z --> BB[Word]
    Z --> CC[PowerPoint]
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