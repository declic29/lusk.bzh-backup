FROM python:3.11-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    git build-essential libxslt-dev libxml2-dev libffi-dev \
    libssl-dev zlib1g-dev libyaml-dev libjpeg-dev shared-mime-info \
    && apt-get clean

# Crée un utilisateur non-root
RUN useradd -m searxng
USER searxng

# Cloner ton fork (optionnel si code déjà présent via GitHub)
WORKDIR /app

# Copier tout le code du repo dans /app
COPY --chown=searxng . .

# Installer les dépendances Python
RUN pip install --upgrade pip \
    && pip install .

# Expose le port (configurable dans settings.yml aussi)
EXPOSE 8080

# Commande de lancement
CMD ["python", "-m", "searx.webapp"]
