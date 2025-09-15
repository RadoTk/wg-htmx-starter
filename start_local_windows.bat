@echo off
echo ========================================
echo   Environnement de développement local Windows
echo   Port: 8080 (différent de Docker: 8000)
echo   Base de données: SQLite locale
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
    echo.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
echo.

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements\development.txt
echo.

REM Appliquer les migrations
echo Application des migrations...
set DJANGO_SETTINGS_MODULE=bakerydemo.settings.local_windows
python manage.py migrate
echo.

REM Collecter les fichiers statiques
echo Collecte des fichiers statiques...
python manage.py collectstatic --noinput
echo.

REM Créer un superutilisateur si nécessaire
echo Création du superutilisateur (optionnel)...
echo Utilisateur: admin
echo Mot de passe: admin123
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
echo.

REM Démarrer le serveur de développement Django (pas WSGI)
echo Démarrage du serveur de développement Django sur http://localhost:8080
echo Interface admin: http://localhost:8080/admin
echo Utilisateur: admin / Mot de passe: admin123
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.
echo Note: Utilise le serveur de développement Django (pas WSGI)
echo Cela évite les conflits avec la configuration Docker
echo.
python manage.py runserver 8080 --settings=bakerydemo.settings.local_windows

pause