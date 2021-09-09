# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies

from core.exception import excpetion_handler

from models.user import UserModel

ENDPOINT = '@RESTFUL_PREFIX::/logout'

class UserLogout(Resource):

    @jwt_required()
    @excpetion_handler
    def get(self):
        response = jsonify({"message": "Logged out successful"})
        unset_jwt_cookies(response)
        return response
