#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
"""WebApp"""

import os
import requests
from flask import render_template, redirect, url_for

from searx.webadapter import get_selected_categories
from searx.extended_types import sxng_request

# L'objet `app` est déjà défini plus loin dans le code. On déclare la route après sa définition.
# Donc on n'ajoute pas de `from searx.webapp import app` (cela cause une erreur de type ImportError circulaire).

# On déplacera cette route à la fin, après l'initialisation de `app`.
# Voici uniquement le contenu de la fonction `index`, sans le décorateur.
def index():
    # redirection si une recherche est faite
    if sxng_request.form.get('q'):
        query = ('?' + sxng_request.query_string.decode()) if sxng_request.query_string else ''
        return redirect(url_for('search') + query, 308)

    # Appel à GNews
    GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY")
    url = f"https://gnews.io/api/v4/search?q=bretagne&lang=fr&country=fr&max=6&apikey={GNEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
    except Exception as e:
        print(f"[ACTUALITÉS BRETAGNE] Erreur : {e}")
        articles = []

    return render_template(
        'index.html',
        selected_categories=get_selected_categories(sxng_request.preferences, sxng_request.form),
        current_locale=sxng_request.preferences.get_value("locale"),
        articles=articles
    )

# À la toute fin du fichier, après avoir défini l'objet `app`, on ajoute :
# app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
# Initialisation de l’application SearXNG
init()

# Ajout manuel de la route principale vers la fonction index
# (cela évite le décorateur @app.route('/') plus haut dans le fichier)
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

# Entrée point WSGI si nécessaire
application = app
