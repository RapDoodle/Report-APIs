# -*- coding: utf-8 -*-
"""This module provides provides a simple HTTP(S) server.

Note:
    It is not recommended to serve the frontend in this manner
    for the sake of performance and security concerns. 
    According to Flask's official documentation, it is of best
    practice to activate your webserver's `X-Sendfile` support.

    For more information, visit:
    https://flask.palletsprojects.com/en/1.1.x/api/#flask.send_from_directory

WARNING:
    Using this HTTP server in production mode will bring huge
    security risks and may result in the server being exploited.

Example:
    init_http_server(app)

"""

from os import path

from flask import Blueprint
from flask import redirect
from flask import current_app
from flask import send_from_directory

from utils.constants import SERVE_FOLDER

DEFAULT_404 = """<h1 style="text-align:center;">404 Not Found</h1>
<hr><p style="text-align:center;">
The application is unable to find the specified file on the server.</p>
<p style="text-align:center;">Mangee Server v1.0</p>"""

server = Blueprint('http_server', __name__)

def init_http_server(app):
    # Show warning on load
    print(' * WARNING: Do NOT use this HTTP server in production!')

    # Configure default values when not specified.
    if app.config.get('HTTP_SERVER_INDEX_PAGE', None) is None:
        app.config['HTTP_SERVER_INDEX_PAGE'] = 'index.html'
    if app.config.get('HTTP_SERVER_INDEX_REDIRECT', None) is None:
        app.config['HTTP_SERVER_INDEX_REDIRECT'] = True
    if app.config.get('HTTP_SERVER_REWRITE_ENGINE', None) is None:
        app.config['HTTP_SERVER_REWRITE_ENGINE'] = False

    app.register_blueprint(server)


@server.route('/', defaults={'filename': ''})
@server.route('/<path:filename>', methods=['GET'])
def index(filename):
    """Mapping of the root directory"""
    if len(filename) == 0 and current_app.config['HTTP_SERVER_INDEX_REDIRECT']:
        # For example, redirect '/' to 'index.html'
        return redirect(current_app.config['HTTP_SERVER_INDEX_PAGE'], code=302)
    return server_router('.', filename)


@server.route('/<path:folder>/<path:file_path>', methods=['GET'])
def send_static_file(folder, file_path):
    return server_router(folder, file_path)


@server.errorhandler(404)
def not_found_handler(e):
    if current_app.config['HTTP_SERVER_REWRITE_ENGINE']:
        return server_router('.', current_app.config.get('HTTP_SERVER_REWRITE_TO'))
    redirect_path = current_app.config.get('HTTP_SERVER_404_REDIRECT', None)
    if redirect_path is not None:
        return redirect(redirect_path, code=302)
    return DEFAULT_404


def server_router(folder, file_path):
    if path.exists(f'./{SERVE_FOLDER}/{folder}/{file_path}'):
        return send_from_directory(directory=f'./{SERVE_FOLDER}/{folder}', 
            filename=file_path)
    if current_app.config['HTTP_SERVER_REWRITE_ENGINE']:
        return send_from_directory(directory=SERVE_FOLDER, 
            filename=current_app.config['HTTP_SERVER_INDEX_PAGE'])