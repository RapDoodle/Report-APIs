# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from core.lang import get_str
from core.exception import excpetion_handler

from models.demo import DemoModel

ENDPOINT = '@RESTFUL_PREFIX::/demo'

class DemoResource(Resource):
    add_parser = reqparse.RequestParser()
    add_parser.add_argument('value',
                        type=str,
                        required=True
                        )

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('id',
                        type=int,
                        required=False
                        )
    get_parser.add_argument('value',
                        type=str,
                        required=False
                        )

    @jwt_required()
    @excpetion_handler
    def post(self):
        data = DemoResource.add_parser.parse_args()

        demo_obj = DemoModel(data['value'])
        demo_obj.save()

        return {'message': get_str('ADDED', obj_name=demo_obj.value)}, 201

    @excpetion_handler
    def get(self):
        data = DemoResource.get_parser.parse_args()

        res = DemoModel.search(_id=data['id'], value=data['value'])
        if res and len(res[0]) > 0:
            jsoned = [obj.json() for obj in res[0]]
            return {'result': jsoned}, 200
        
        return '', 204

    @jwt_required()
    @excpetion_handler
    def delete(self):
        data = DemoResource.get_parser.parse_args()
        
        res = DemoModel.find_by_id(_id=data['id'])
        if res is not None and isinstance(res, DemoModel):
            res.delete()
            return {'message': get_str('DELETED', obj_name=res.value)}, 200

        return {'message': get_str('NOT_FOUND')}, 200
