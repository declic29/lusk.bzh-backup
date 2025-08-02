#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
"""WebApp"""

# --- Suppression du doublon de route '/' ---
# Tu avais deux fois `@app.route('/') def index()`, ce qui causait le plantage sur Koyeb.
# Le code ci-dessous conserve la version correcte qui affiche les articles de GNews
# et supprime la version de l'index HTML par défaut.
# Le bloc corrigé est replacé plus bas pour éviter le conflit d'import.

import os
import requests
from flask import render_template

# Version correcte et unique de la route '/'
@app.route('/', methods=['GET', 'POST'])
def index():
    from searx.webadapter import get_selected_categories
    from searx.extended_types import sxng_request

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

    return render(
        'index.html',
        selected_categories=get_selected_categories(sxng_request.preferences, sxng_request.form),
        current_locale=sxng_request.preferences.get_value("locale"),
        articles=articles
    )
