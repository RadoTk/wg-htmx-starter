# Script PowerShell pour environnement de développement local Windows
# Utilise des ports et configurations différents de Docker

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Environnement de développement local Windows" -ForegroundColor Green
Write-Host "  Port: 8080 (différent de Docker: 8000)" -ForegroundColor Green
Write-Host "  Base de données: SQLite locale" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python détecté: $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "Erreur: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel si nécessaire
if (-not (Test-Path "venv")) {
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host ""
}

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host ""

# Installer les dépendances
Write-Host "Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements\development.txt
Write-Host ""

# Configurer les variables d'environnement
$env:DJANGO_SETTINGS_MODULE = "rootapp.settings.local_windows"

# Appliquer les migrations
Write-Host "Application des migrations..." -ForegroundColor Yellow
python manage.py migrate
Write-Host ""

# Collecter les fichiers statiques
Write-Host "Collecte des fichiers statiques..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host ""

# Créer un superutilisateur si nécessaire
Write-Host "Vérification du superutilisateur..." -ForegroundColor Yellow
$createUserScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur existe déjà: admin/admin123')
"@

python manage.py shell -c $createUserScript
Write-Host ""

# Démarrer le serveur de développement Django (pas WSGI)
Write-Host "Démarrage du serveur de développement Django sur http://localhost:8080" -ForegroundColor Green
Write-Host "Interface admin: http://localhost:8080/admin" -ForegroundColor Green
Write-Host "Utilisateur: admin / Mot de passe: admin123" -ForegroundColor Green
Write-Host ""
Write-Host "Note: Utilise le serveur de développement Django (pas WSGI)" -ForegroundColor Cyan
Write-Host "Cela évite les conflits avec la configuration Docker" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 8080 --settings=rootapp.settings.local_windows
