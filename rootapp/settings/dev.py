from .base import *  # noqa: F403, F401

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# WAGTAILADMIN_BASE_URL required for notification emails
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")


ALLOWED_HOSTS = ["*"]

try:
    from .local import *  # noqa
except ImportError:
    pass
