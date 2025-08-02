#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
"""WebApp"""

import os
import sys
import requests
from flask import render_template, redirect, url_for

from searx.webadapter import get_selected_categories
from searx.extended_types import sxng_request
from searx.webapp import app, render, patch_application
from searx import favicons, searx_plugins, search
from searx.plugins import limiter
from searx.settings_loader import get_setting, DEFAULT_SETTINGS_FILE, settings
from searx.languages import LOCALE_NAMES, LOCALE_BEST_MATCH, get_locale, locales_initialize
from searx.brand import GIT_BRANCH, GIT_URL, VERSION_STRING
from searx.utils import logger
from searx.engines import engines, categories, checker_get_result
from searx.stats import get_engines_stats, get_engine_errors, get_reliabilities, STATS_SORT_PARAMETERS
from searx.metrics import openmetrics
from searx.valkey_init import valkey_initialize

from werkzeug.datastructures import Headers
from werkzeug.middleware.shared_data import SharedDataMiddleware
from whitenoise import WhiteNoise
from flask import Response, send_from_directory, make_response

# Déclaration de la fonction index() (sans décorateur ici)
def index():
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


def static_headers(headers: Headers, _path: str, _url: str) -> None:
    headers['Cache-Control'] = 'public, max-age=30, stale-while-revalidate=60'
    for header, value in settings['server']['default_http_headers'].items():
        headers[header] = value


def init():
    if searx.sxng_debug or app.debug:
        app.debug = True
        searx.sxng_debug = True

    if not app.debug and get_setting("server.secret_key") == 'ultrasecretkey':
        logger.error("server.secret_key is not changed. Please use something else instead of ultrasecretkey.")
        sys.exit(1)

    locales_initialize()
    valkey_initialize()
    searx_plugins.initialize(app)

    metrics = get_setting("general.enable_metrics")
    search.initialize(enable_checker=True, check_network=True, enable_metrics=metrics)

    limiter.initialize(app, settings)
    favicons.init()


# Application WSGI avec fichiers statiques et headers personnalisés
app.wsgi_app = WhiteNoise(
    app.wsgi_app,
    root=settings['ui']['static_path'],
    prefix="static",
    max_age=None,
    allow_all_origins=False,
    add_headers_function=static_headers,
)

patch_application(app)
init()

# Liaison manuelle de la route index après l'init
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

application = app
