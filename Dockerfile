FROM python:3.12-slim
ARG NIGHTLY=0

# 1️⃣ Installer les dépendances système
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
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Copier les requirements et créer un environnement virtuel
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

# 3️⃣ Copier le code
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# 4️⃣ Entrypoint
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh

# 5️⃣ Ports exposés et variables d'environnement
ENV PORT=8000
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=rootapp.settings.production DJANGO_DEBUG=off

# 6️⃣ Collectstatic (facultatif, utile pour production)
RUN DATABASE_URL=postgres://none REDIS_URL=none python manage.py collectstatic --noinput

# 7️⃣ Préparer les dossiers pour les fichiers médias
RUN mkdir -p /code/rootapp/media/images /code/rootapp/media/original_images \
    && chown -R 1000:2000 /code/rootapp/media

VOLUME ["/code/rootapp/media/images/"]

# 8️⃣ Entrypoint + CMD pour Daphne
ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "rootapp.asgi:application"]
