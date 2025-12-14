"""
Test environment settings for clinical_case_platform project.
Optimized for Vietnamese medical education platform - Test Environment.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-dev-key-change-in-production"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,0.0.0.0",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_extensions",
    "drf_spectacular",
]

LOCAL_APPS = [
    "accounts",
    "cases",
    "templates",
    "repositories",
    "comments",
    "feedback",
    "exports",
    "grades",
    "notifications.apps.NotificationsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "clinical_case_platform.middleware.ResponseCompressionMiddleware",  # Gzip compression
    "django.contrib.sessions.middleware.SessionMiddleware",
    "clinical_case_platform.middleware.CacheControlMiddleware",  # Smart caching
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "clinical_case_platform.middleware.SecurityHeadersMiddleware",  # Security headers
    "clinical_case_platform.middleware.RequestTimingMiddleware",  # Performance monitoring
]

ROOT_URLCONF = "clinical_case_platform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "clinical_case_platform.wsgi.application"

# Database - Test database configuration with optimization
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME_TEST", default="clinical_case_platform_test"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        # For Hoang An's local Arch setup.
        # "USER": config("DB_USER", default="martelle"),
        # "PASSWORD": config("DB_PASSWORD", default="martelle123"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
        # Connection pooling for better performance
        "CONN_MAX_AGE": 300,  # 5 minutes - shorter for testing
        "OPTIONS": {
            "connect_timeout": 30,
            "options": "-c statement_timeout=30000",  # 30 second query timeout
        },
        # Enable atomic requests for data integrity
        "ATOMIC_REQUESTS": True,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization - Vietnamese settings
LANGUAGE_CODE = "vi-vn"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files for test environment
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_test"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Django REST Framework - Test environment with browsable API
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Enable browsable API for testing
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Rate limiting / throttling for test environment
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/hour",  # More lenient for testing
        "user": "2000/hour",  # More lenient for testing
        "login": "10/minute",  # Login attempts
        "export": "20/hour",  # Export operations
        "upload": "50/hour",  # File uploads
    },
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}

# CORS settings for frontend development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vue.js development server
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite development server
    "http://127.0.0.1:5173",
]

CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
    'pragma',
    'expires',
]

# Redis settings (temporarily disabled for development)
# REDIS_URL = config('REDIS_URL', default='redis://localhost:6379')

# Cache configuration for test environment - Using LocMemCache (no Redis required)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-clinical-case-platform",
        "TIMEOUT": 300,  # 5 minutes default
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
        }
    }
}

# For production, uncomment below to use Redis:
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/2",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "CONNECTION_POOL_KWARGS": {
#                 "max_connections": 30,
#                 "retry_on_timeout": True,
#                 "socket_keepalive": True,
#                 "socket_connect_timeout": 5,
#             },
#             "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#             "SOCKET_CONNECT_TIMEOUT": 5,
#             "SOCKET_TIMEOUT": 5,
#         },
#         "KEY_PREFIX": "test_ccp",
#         "TIMEOUT": 300,
#     }
# }

# Cache TTL settings for different data types (test environment)
CACHE_TTL = {
    "case_list": 180,  # 3 minutes for testing
    "case_detail": 120,  # 2 minutes
    "user_data": 180,  # 3 minutes
    "statistics": 120,  # 2 minutes for faster test iterations
    "notifications": 30,  # 30 seconds
    "static_data": 600,  # 10 minutes
}

# Email settings
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# API Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Clinical Case Management Platform API - Test Environment",
    "DESCRIPTION": "API for managing medical student case documentation and collaboration",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Logging for test environment - Enhanced with rotation and error tracking
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django_test.log",
            "formatter": "verbose",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django_test_errors.log",
            "formatter": "verbose",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "cases": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}

# Celery configuration for test environment (optional - only if Redis is running)
# CELERY_BROKER_URL = "redis://127.0.0.1:6379/2"
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes for testing
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes soft limit

# Celery Beat Schedule - Test environment (optional, can be disabled)
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "cleanup-old-case-data": {
        "task": "cases.tasks.cleanup_old_case_data",
        "schedule": crontab(hour=3, minute=0),  # 3 AM daily
    },
    "generate-department-analytics": {
        "task": "cases.tasks.generate_department_analytics",
        "schedule": crontab(hour=4, minute=0),  # 4 AM daily
    },
}

print("🧪 Using TEST environment settings")
print(f"📊 Database: {DATABASES['default']['NAME']}")
print(f"📁 Media: {MEDIA_ROOT}")
