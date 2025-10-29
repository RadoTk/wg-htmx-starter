# 1️⃣ Base image Python
FROM python:3.12-slim
ARG NIGHTLY=0

# 2️⃣ Installer les dépendances système
RUN set -ex \
    && RUN_DEPS=" \
        libexpat1 \
        libjpeg62-turbo \
        libpcre2-posix3 \
        libpq5 \
        shared-mime-info \
        postgresql-client \
        procps \
        zlib1g \
        libssl-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Ajouter et installer les dépendances Python
ADD requirements/ /requirements/
ENV VIRTUAL_ENV=/venv PATH=/venv/bin:$PATH PYTHONPATH=/code/

RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        curl \
        git \
        libexpat1-dev \
        libjpeg62-turbo-dev \
        libpcre2-dev \
        libpq-dev \
        zlib1g-dev \
        redis-tools \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && if [ "$NIGHTLY" = "1" ]; then \
        NIGHTLY_URL=$(curl -s https://releases.wagtail.org/nightly/latest.json | \
            grep -o 'https://[^"]*') \
        && sed -i "s|wagtail>=.*|${NIGHTLY_URL}|" /requirements/base.txt; \
    fi \
    && python3.12 -m venv ${VIRTUAL_ENV} \
    && python3.12 -m pip install -U pip \
    && python3.12 -m pip install --no-cache-dir -r /requirements/production.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copier le code source dans l'image
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# 5️⃣ Entrypoint (script d'entrée personnalisé)
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh

# 6️⃣ Configurer les variables d'environnement et exposer le port
ENV PORT=8000
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=rootapp.settings.production DJANGO_DEBUG=off

# 7️⃣ Collecter les fichiers statiques à l'avance (facultatif, utile en production
WORKDIR /code
ENV DJANGO_SETTINGS_MODULE=rootapp.settings.production
RUN DATABASE_URL=postgres://none REDIS_URL=none python manage.py collectstatic --noinput

# 8️⃣ Préparer les dossiers pour les fichiers médias
RUN mkdir -p /code/rootapp/media/images /code/rootapp/media/original_images \
    && chown -R 1000:2000 /code/rootapp/media

VOLUME ["/code/rootapp/media/images/"]

# 9️⃣ Démarrer le serveur avec Daphne (ASGI)
ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "rootapp.asgi:application"]
