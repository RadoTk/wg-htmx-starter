"""Configuration WSGI spécifique pour l'environnement de développement local Windows.

Ce fichier évite les conflits avec la configuration Docker et utilise
des paramètres optimisés pour le développement local.
"""

import os
from pathlib import Path

# Charger les variables d'environnement depuis .env.local
try:
    from dotenv import load_dotenv
    # Charger d'abord .env.local puis .env comme fallback
    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir / ".env.local")
    load_dotenv(base_dir / ".env")
except ImportError:
    # Si python-dotenv n'est pas installé, continuer sans
    pass

# Configuration par défaut pour l'environnement Windows local
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootapp.settings.local_windows")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Créer l'application WSGI
application = get_wsgi_application()
