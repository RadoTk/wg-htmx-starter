#!/bin/sh
set -e

# 1️⃣ Attendre que Postgres soit prêt
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# 2️⃣ Appliquer les migrations
/venv/bin/python manage.py migrate --noinput

# 3️⃣ Charger les données initiales si demandé
if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
    /venv/bin/python manage.py load_initial_data
fi

# 4️⃣ Lancer Daphne
exec "$@"
