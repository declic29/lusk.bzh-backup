# --------- Étape 1 : base de construction ---------
FROM python:3.11-slim as builder

# Dépendances système minimales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential libxslt-dev libffi-dev libxml2-dev zlib1g-dev \
        libjpeg-dev libyaml-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Variables personnalisables (tu peux changer si nécessaire)
ARG SEARXNG_REPO=https://github.com/searxng/searxng.git
ARG SEARXNG_BRANCH=main

# Dossier de destination du code
ENV SEARXNG_SRC=/usr/local/searxng

# Clone du dépôt
RUN git clone --depth=1 --branch ${SEARXNG_BRANCH} ${SEARXNG_REPO} ${SEARXNG_SRC}

# Installation des dépendances Python
WORKDIR ${SEARXNG_SRC}
RUN pip install --upgrade pip setuptools && pip install .

# --------- Étape 2 : Image finale allégée ---------
FROM python:3.11-slim

ENV SEARXNG_SRC=/usr/local/searxng
ENV INSTANCE_NAME="lusk.bzh"

# Copie depuis l’image builder
COPY --from=builder ${SEARXNG_SRC} ${SEARXNG_SRC}
WORKDIR ${SEARXNG_SRC}

# Copie de tes personnalisations (à adapter si tu ajoutes un dossier `custom`)
# Exemple : templates personnalisés, settings.yml, favicon, etc.
COPY ./
