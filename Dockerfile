# --------- Étape 1 : base de construction ---------
FROM python:3.13-slim as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential libxslt-dev libffi-dev libxml2-dev zlib1g-dev \
        libjpeg-dev libyaml-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG SEARXNG_REPO=https://github.com/searxng/searxng.git
ARG SEARXNG_BRANCH=main
ENV SEARXNG_SRC=/usr/local/searxng

RUN git clone --depth=1 --branch ${SEARXNG_BRANCH} ${SEARXNG_REPO} ${SEARXNG_SRC}
WORKDIR ${SEARXNG_SRC}
RUN pip install --upgrade pip setuptools && pip install .

# --------- Étape 2 : Image finale ---------
FROM python:3.13-slim

ENV SEARXNG_SRC=/usr/local/searxng
ENV INSTANCE_NAME="lusk.bzh"
ENV PORT=8080

COPY --from=builder ${SEARXNG_SRC} ${SEARXNG_SRC}
WORKDIR ${SEARXNG_SRC}

# Copie ton settings.yml si besoin
COPY ./settings.yml ./settings.yml

# Port exposé pour Koyeb
EXPOSE ${8080}

# ✅ Ligne unique pour démarrer SearXNG proprement
CMD ["gunicorn", "-b", "0.0.0.0:8080", "searx.webapp:app"]
