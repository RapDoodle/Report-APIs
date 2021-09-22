# -*- coding: utf-8 -*-
import datetime

from core.db import db


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(64))
    message = db.Column(db.String(1024))
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    ip = db.Column(db.String(64))

    def __init__(self, label, message, ip=''):
        # Clean the data
        label = str(label).strip()
        message = str(message).strip()
        ip = str(ip).strip()

        # Store the data in the object
        self.label = label
        self.message = message
        self.ip = ip

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'value': self.value}

    def __repr__(self):
        return f'<Demo(id={self.id}, value="{self.value}")>'

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(value=value).all()
        
