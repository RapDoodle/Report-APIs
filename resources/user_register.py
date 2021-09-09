# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask_restful import reqparse

from core.exception import excpetion_handler

from models.user import UserModel

ENDPOINT = '@RESTFUL_PREFIX::/register'

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='The username of the user cannot be empty.'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='The password field cannot be empty.'
                        )

    @excpetion_handler
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save()

        return {'message': 'User created successfully.'}, 201
