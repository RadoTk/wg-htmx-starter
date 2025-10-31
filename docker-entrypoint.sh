#!/bin/sh
set -e

# Vérifier que DATABASE_URL est défini
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set. Please define the database URL." >&2
    exit 1
fi

# Attente que PostgreSQL soit disponible
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# 2️⃣ Appliquer les migrations
echo "Applying migrations..."
/venv/bin/python manage.py migrate --noinput


# 3️⃣ Exécuter les commandes personnalisées pour créer des pays et des statuts
echo "Creating default countries..."
/venv/bin/python manage.py create_default_countries
echo "Creating default statuses..."
/venv/bin/python manage.py create_default_statuses

# 3️⃣ Charger les données initiales si demandé
if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
    echo "Loading initial data..."
    /venv/bin/python manage.py load_initial_data
fi

# 4️⃣ Lancer Daphne
echo "Starting Daphne server..."
exec "$@"
