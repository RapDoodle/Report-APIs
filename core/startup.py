# -*- coding: utf-8 -*-
"""The module provides functions related to startup routines."""

import os
import re
import logging
from json import loads
from datetime import timedelta

from flask import Flask
from flask_restful import Api

from settings import IMPORT_RESOURCES
from core.jwt import init_jwt
from core.db import db
from core.db import init_db
from core.lang import init_lang
from utils.constants import CONFIG_PATH


def create_app(name: str, config_name: str) -> Flask:
    """Creates a flask object based on configurations.

    Note:
        This function does not start the server. It only 
        creates a Flask object.

    Args:
        name (str): The name of the application, in the most
            cases, please use __name__. For more information,
            please vist:
            https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask
        config_name (str): The name of the configuration

    Returns:
        flask.app.Flask: The configured flask application.

    """
    config = load_config(config_name)
    app = Flask(name)

    # Set configuration into the app
    for key in config.keys():
        app.config[key] = config[key]
        
    # Initialize core modules
    init_core_modules(app)

    # Dynamically load all resources
    load_resources(app)
    return app


def init_core_modules(app):
    """Initializes the core modules for the given context.

    It initializes the following plugins/functions in order:
        1). Launguage system
        2). Logger
        3). Flask-JWT-Extended
        4). Flask-SQLAlchemy
        5). HTTP server (testing only)
    
    Args:
        app (flask.app.Flask): A Flask application.

    """
    # Initialize the launguage system.
    init_lang(app)

    # Setup logger
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(app.config.get('LOG_FORMAT', \
            '%(asctime)s %(levelname)s: %(message)s')))
    app.logger.addHandler(file_handler)

    # Setting up flask-JWT
    init_jwt(app)

    # Setup database
    init_db(app)
    with app.app_context():
        db.create_all()

    # Simple HTTP server. Not recommended in production.
    if (app.config.get('ENABLE_SIMPLE_HTTP_SERVER', False)):
        from utils.http_server import init_http_server
        init_http_server(app)


def load_resources(app):
    """Imports resources dynamically.

    This function will automatically add all the resources 
    specified in `IMPORT_RESOURCES` of `settings.py`.

    Note:
        In order to import the resources properly, the object
        inherited from `Resource` must be named in the module 
        name's camel-case. For example, the module name of
        `user_register` should have a class `UserRegister`.
        Additionally, a variable named `ENDPOINT` must be
        specified in the module to inidicate the enpoint in
        which the resource will be attached to. 

    Args:
        app (flask.app.Flask): A Flask application.

    """
    api = Api(app)
    for resource in IMPORT_RESOURCES:
        # From snake case to camel case
        resource_class_name = ''.join([n.capitalize() \
            for n in resource.split('_')])

        # Import modules dynamically
        resource_module = __import__(f'resources.{resource}', fromlist=[resource])
        resource_class = getattr(resource_module, resource_class_name)
        endpoint = getattr(resource_module, 'ENDPOINT')
        endpoint = re.sub('@(RESTFUL_PREFIX)::*', \
                    app.config['RESTFUL_PREFIX'], endpoint)
        api.add_resource(resource_class, endpoint)


def load_config(name: str) -> dict:
    """Reads and parses configuration and returns as a dict.

    Args:
        name (str): The name of the configuration. By default, 
        it should be stored in `/config` and should be a 
        json file.

    Example:
        By default, using ``load_config(name='dev')``, the 
        function reads the configuration in
        ``./configurations/dev.json``. To change the directory 
        to store the configurations, please change `CONFIG_PATH`.

    Returns:
        dict: The file in the form of python dictionary.
    
    """
    config_raw = loads(open(os.path.join(CONFIG_PATH, name+'.json'), 'r').read())
    config_parsed = {}

    # Parser for configurations
    for key in config_raw.keys():
        if key.startswith('@'):
            # Parser of special configuration
            value = config_raw[key]
            if isinstance(value, dict):
                # Cases where direct parsing is not possible
                func_type = value['type']
                if func_type == 'timedelta':
                    assert isinstance(value['args'], dict)
                    value = timedelta(**value['args'])
            elif isinstance(value, str):
                # Reference with '@'
                value = re.sub('@(RESTFUL_PREFIX)::*', \
                    config_raw['RESTFUL_PREFIX'], config_raw[key])
            # Remove the prefix '@' before storing into the config
            config_parsed[key[1:]] = value
            continue
        config_parsed[key] = config_raw[key]
    return config_parsed


def run(app):
    """Spins up a Flask application (development server).
    
    Args:
        app (flask.app.Flask): A Flask application

    """
    if app.config.get('ENABLE_HTTPS', False):
        ssl_context = (
            app.config.get('HTTPS_CERT_PATH'), 
            app.config.get('HTTPS_PRIVATE_KEY_PATH'))
    else:
        ssl_context = None
    app.run(
        host=app.config.get('HOST', '127.0.0.1'), 
        port=app.config.get('PORT', 5000),
        ssl_context=ssl_context)