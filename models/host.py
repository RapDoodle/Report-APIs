# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

from core.db import db


class Host(db.Model):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))
    ip = db.Column(db.String(64))
    message = db.Column(db.String(1024))
    last_received = db.Column(db.DateTime, default=datetime.now)
    

    def __init__(self, ip, name, message=''):
        # Clean the data
        name = str(name).strip()
        message = str(message).strip()
        ip = str(ip).strip()

        # Store the data in the object
        self.name = name
        self.message = message
        self.ip = ip

    def update(self, message='', name=None, update_name=False):
        if update_name:
            self.name = name
        self.message = message
        self.last_received = datetime.now()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'value': self.value}

    @classmethod
    def find_host_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_host_by_ip(cls, ip):
        return cls.query.filter_by(ip=ip).first()

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(value=value).all()
        
    @classmethod
    def get_online_hosts(cls, timeout=3600):
        timeout_time = datetime.now() - timedelta(seconds=timeout)
        return cls.query.filter(cls.last_received >= timeout_time).order_by(cls.name).all()

