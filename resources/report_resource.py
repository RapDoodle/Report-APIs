# -*- coding: utf-8 -*-
from datetime import datetime
from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from core.lang import get_str
from core.exception import excpetion_handler

from models.report import Report

ENDPOINT = '@RESTFUL_PREFIX::/v1/report'

class ReportResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('message',
                        type=str,
                        required=True
                        )
    post_parser.add_argument('label',
                        type=str,
                        required=False
                        )

    @excpetion_handler
    def post(self):
        data = ReportResource.post_parser.parse_args()
        
        ip = request.remote_addr
        label = data['label'].strip()
        message = data['message'].strip()
        dt_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = Report(label=label, message=message, ip=ip)
        report.save()
        
        print(f"[{dt_str}][{label}] From {ip}: ")
        print(message)

        if data['label'] is not None:
            with open(f"./logs/{label} {ip}.txt", 'ab') as file:
                file.write(f"\n[{dt_str}] From {request.remote_addr}:\n".encode('UTF-8'))
                file.write(message.encode('UTF-8'))

        return {'message': 'Success'}, 201


