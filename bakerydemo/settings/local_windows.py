from .base import *  # noqa: F403, F401
import os

# Configuration pour développement local Windows
# Utilise des ports différents de Docker pour éviter les conflits

DEBUG = True

# Configuration WSGI spécifique pour Windows local
WSGI_APPLICATION = 'bakerydemo.wsgi_local_windows.application'

# Base de données SQLite locale (pas de conflit avec PostgreSQL Docker)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local_windows.sqlite3'),
    }
}

# Configuration email pour développement
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# URL de base pour l'admin Wagtail (port différent de Docker)
WAGTAILADMIN_BASE_URL = "http://localhost:8080"

# Hosts autorisés
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# Désactiver Redis pour l'environnement local (optionnel)
# Utiliser le cache en mémoire à la place
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Configuration de développement spécifique à Windows
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_local')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_local')

# Désactiver HTTPS en développement local
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configuration pour le serveur de développement local
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Logging pour développement
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Essayer d'importer les paramètres locaux personnalisés
try:
    from .local import *  # noqa
except ImportError:
    pass