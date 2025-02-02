from .base import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

DEBUG = False
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [
#                        s.strip() for s in v.split(",")])
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]


# Cloudinary Configuration For Serving Media Files
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = f'https://res.cloudinary.com/{config('CLOUD_NAME')}/'

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

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
