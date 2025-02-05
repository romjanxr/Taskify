from .base import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

DEBUG = False

# Whitenoise for Static Files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
    }
}

# Ensure WhiteNoiseMiddleware comes after SecurityMiddleware
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') +
                  1, "whitenoise.middleware.WhiteNoiseMiddleware")

FRONTEND_URL = "https://djtaskify.vercel.app"

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
