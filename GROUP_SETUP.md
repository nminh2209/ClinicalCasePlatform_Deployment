# Group Development Setup Guide

## For Each Team Member

### 1. Database Setup

- Create your own PostgreSQL database:

  ```sql
  CREATE DATABASE clinical_case_platform_yourname;
  ```

### 2. Environment Setup

- Copy `.env.template` to `.env`
- Update `DB_NAME` with your name: `clinical_case_platform_yourname`
- Set your PostgreSQL password
- Generate your own SECRET_KEY

### 3. Django Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Git Branch Strategy

- Create your own feature branch:

  ```bash
  git checkout -b feature/yourname-development
  ```

## Database Names by Team Member

- **Minh**: `clinical_case_platform_minh`
- **Member 2**: `clinical_case_platform_member2`
- **Member 3**: `clinical_case_platform_member3`
- **Main/Shared**: `clinical_case_platform` (for integration testing)

## Important Notes

- Never commit your `.env` file
- Each person has their own database
- Use branches for feature development
- Merge to `develop` branch for integration testing

