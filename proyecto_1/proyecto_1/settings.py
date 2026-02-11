import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Seguridad
# =========================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-key-only-local"
)

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "18.188.190.104",  # <-- tu IP pública EC2
]


# =========================
# Media (tus PDFs/Excels)
# =========================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================
# Static
# =========================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================
# Apps
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]


# =========================
# Database (SQLite)
# =========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# Otros
# =========================

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
