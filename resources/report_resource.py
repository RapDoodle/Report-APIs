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

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('template',
                        type=str,
                        required=True
                        )
    put_parser.add_argument('label',
                        type=str,
                        required=False
                        )

    @excpetion_handler
    def post(self):
        data = ReportResource.post_parser.parse_args()

        report = Report(label=data['label'], message=data['message'], ip=request.remote_addr)
        report.save()

        if data['label'] is not None:
            with open(f"./logs/{data['label']}.txt", 'ab') as file:
                file.write(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] From {request.remote_addr}:\n".encode('UTF-8'))
                file.write(data['message'].encode('UTF-8'))

        return {'message': 'Success'}, 201


