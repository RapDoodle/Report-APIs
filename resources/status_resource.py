# -*- coding: utf-8 -*-
from datetime import datetime
from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from core.lang import get_str
from core.exception import excpetion_handler

from models.host import Host

ENDPOINT = '@RESTFUL_PREFIX::/v1/status'

class StatusResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name',
                        type=str,
                        required=False,
                        default='Unknown'
                        )
    post_parser.add_argument('message',
                        type=str,
                        required=False,
                        default=''
                        )
    post_parser.add_argument('update_name',
                        type=bool,
                        required=False,
                        default=False
                        )

    @excpetion_handler
    def post(self):
        data = StatusResource.post_parser.parse_args()
        
        ip = request.remote_addr
        name = data['name'].strip()
        message = data['message'].strip()
        update_name = data['update_name']
        dt_str = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        host = Host.find_host_by_ip(ip=ip)

        if host is None:
            host = Host(ip=ip, name=name, message=message)
            host.save()
        else:
            host.update(message=message, name=name, update_name=update_name)

        return {'message': 'Success'}, 201


