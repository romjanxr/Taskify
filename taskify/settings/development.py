from .base import *

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'taskify',
#         'USER': 'postgres',
#         'PASSWORD': 'admin123',
#         'HOST': 'localhost',
#         'PORT': 5432
#     }
# }

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

INSTALLED_APPS += [
    "debug_toolbar"
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]

STATICFILES_DIRS = [BASE_DIR / "static"]

FRONTEND_URL = "http://127.0.0.1:8000"
