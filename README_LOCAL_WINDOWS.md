# Environnement de Développement Local Windows

Ce guide vous permet de configurer un environnement de développement local sur Windows qui coexiste parfaitement avec l'environnement Docker sans conflits.

## 🎯 Avantages de cette configuration

- **Pas de conflits avec Docker** : Utilise le port 8080 au lieu de 8000
- **Base de données SQLite** : Pas besoin de PostgreSQL local
- **Pas de Redis requis** : Utilise le cache mémoire
- **Configuration isolée** : Fichiers de configuration séparés
- **Démarrage rapide** : Scripts automatisés

## 📋 Prérequis

- Python 3.8+ installé sur Windows
- Git installé
- PowerShell ou Command Prompt

## 🚀 Démarrage rapide

### Option 1 : Script Batch (.bat)
```cmd
# Double-cliquer sur le fichier ou exécuter :
start_local_windows.bat
```

### Option 2 : Script PowerShell (.ps1)
```powershell
# Exécuter dans PowerShell :
.\start_local_windows.ps1
```

### Option 3 : Manuel
```cmd
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement virtuel
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements\development.txt

# 4. Configurer Django
set DJANGO_SETTINGS_MODULE=rootapp.settings.local_windows

# 5. Appliquer les migrations
python manage.py migrate

# 6. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 7. Créer un superutilisateur
python manage.py createsuperuser

# 8. Démarrer le serveur
python manage.py runserver 8080
```

## 🌐 Accès à l'application

- **Site principal** : http://localhost:8080
- **Interface admin** : http://localhost:8080/admin
- **Compte admin par défaut** : admin / admin123

## 📁 Structure des fichiers créés

```
wg-starter/
├── rootapp/settings/local_windows.py    # Configuration Windows
├── .env.local                              # Variables d'environnement locales
├── start_local_windows.bat                 # Script de démarrage Batch
├── start_local_windows.ps1                 # Script de démarrage PowerShell
├── README_LOCAL_WINDOWS.md                 # Ce fichier
├── db_local_windows.sqlite3                # Base de données SQLite (créée automatiquement)
├── staticfiles_local/                      # Fichiers statiques locaux
├── media_local/                            # Fichiers media locaux
└── venv/                                   # Environnement virtuel Python
```

## ⚙️ Configuration

### Ports utilisés
- **Local Windows** : 8080
- **Docker** : 8000
- **Pas de conflit** ✅

### Base de données
- **Local Windows** : SQLite (`db_local_windows.sqlite3`)
- **Docker** : PostgreSQL
- **Données séparées** ✅

### Cache
- **Local Windows** : Cache mémoire Django
- **Docker** : Redis
- **Pas de dépendance Redis** ✅

## 🔧 Personnalisation

### Modifier le port
Éditer `rootapp/settings/local_windows.py` :
```python
WAGTAILADMIN_BASE_URL = "http://localhost:VOTRE_PORT"
```

### Ajouter des variables d'environnement
Éditer `.env.local` :
```env
VOTRE_VARIABLE=valeur
```

### Utiliser PostgreSQL local
Si vous préférez PostgreSQL :
```python
# Dans local_windows.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bakery_local',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5433',  # Port différent de Docker (5432)
    }
}
```

## 🐳 Coexistence avec Docker

### Démarrer Docker (port 8000)
```cmd
docker-compose up
```

### Démarrer local Windows (port 8080)
```cmd
start_local_windows.bat
```

### Les deux peuvent tourner simultanément ! 🎉
- Docker : http://localhost:8000
- Windows : http://localhost:8080

## 🛠️ Commandes utiles

### Réinitialiser la base de données locale
```cmd
del db_local_windows.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Mettre à jour les dépendances
```cmd
venv\Scripts\activate
pip install -r requirements\development.txt --upgrade
```

### Nettoyer l'environnement
```cmd
rmdir /s venv
del db_local_windows.sqlite3
rmdir /s staticfiles_local
rmdir /s media_local
```

## 🚨 Dépannage

### Port 8080 déjà utilisé
```cmd
# Trouver le processus utilisant le port
netstat -ano | findstr :8080
# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

### Erreur de permissions PowerShell
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python non trouvé
- Vérifier que Python est dans le PATH
- Réinstaller Python avec l'option "Add to PATH"

## 📝 Notes importantes

1. **Données séparées** : Les données locales et Docker sont complètement séparées
2. **Pas de conflit** : Vous pouvez utiliser les deux environnements simultanément
3. **Développement rapide** : Pas besoin de rebuilder Docker pour tester des changements
4. **Production** : Utilisez toujours Docker pour la production

## 🤝 Contribution

Pour améliorer cette configuration :
1. Modifier les fichiers de configuration
2. Tester les changements
3. Mettre à jour cette documentation

---

**Bon développement ! 🚀**
