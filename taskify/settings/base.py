from pathlib import Path
from decouple import config
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False  # Default value; override in specific environments

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]
AUTH_USER_MODEL = "users.CustomUser"

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'cloudinary',
    'cloudinary_storage',
    "tasks",
    "users",
    "core",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "taskify.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "taskify.wsgi.application"

# Database will be defined in specific environment files
DATABASES = {}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Cloudinary Configuration For Serving Media Files

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET')
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = f'https://res.cloudinary.com/{config('CLOUD_NAME')}/'
MEDIA_ROOT = BASE_DIR / "media"

cloudinary.config(
    cloud_name=config('CLOUD_NAME'),
    api_key=config('API_KEY'),
    api_secret=config('API_SECRET')
)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "slashupdates@gmail.com"


LOGIN_URL = "/users/sign-in/"
LOGIN_REDIRECT_URL = "/tasks/dashboard/"
LOGOUT_REDIRECT_URL = "/"
