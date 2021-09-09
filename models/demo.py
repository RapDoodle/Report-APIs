# -*- coding: utf-8 -*-
from core.db import db


class DemoModel(db.Model):
    """This is a demo model that should be removed in production.

    Note:
        This is only a demo model provided by the template library
        Magee Flask-RESTful. It should only be used for testing and 
        demo. Please make sure to remove the model in production mode.
        For more information on how to use Flask-SQLAlchemy, visit
        https://flask-sqlalchemy.palletsprojects.com/en/2.x/

    Attributes:
        id (Integer): the object's id
        value (String): a string belongs to the entry

    """
    __tablename__ = 'demo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255))

    def __init__(self, value):
        # Clean the data
        value = str(value).strip()

        # Store the data in the object
        self.value = value

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

    @classmethod
    def search(cls, _id=None, value=None):
        queries = []
        if _id:
            queries.append(DemoModel.id==_id)
        if value:
            queries.append(DemoModel.value==value)
        return [cls.query.filter(*queries).all()]
