# -*- coding: utf-8 -*-
import os
import json
import hashlib
from datetime import datetime
from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import inputs
from flask_jwt_extended import jwt_required

from core.lang import get_str
from core.exception import excpetion_handler

from models.host import Host

ENDPOINT = '@RESTFUL_PREFIX::/v1/profile'

class ProfileResource(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('name',
                            type=str,
                            required=True,
                            )

    @excpetion_handler
    def get(self):
        args = ProfileResource.get_parser.parse_args()
        
        name = args['name'].strip()

        filepath = f'./profiles/{name}.json'

        if not os.path.exists(filepath):
            return {'error': 'Profile not found.'}, 404
        
        with open(filepath) as f:
            try:
                json_data = json.load(f)
                md5 = hashlib.md5(str(json_data).encode('utf8'))
            except json.decoder.JSONDecodeError:
                return {'error': 'The profile contains invalid synxtax.'}

        json_data['MD5'] = md5.hexdigest()

        return json_data, 200

