import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict, NotFound
from werkzeug.routing import BaseConverter

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import Person


JSON = "application/json"

class PersonCollection(Resource):

    def get(self):
        pass

    def post(self):
        pass


class PersonItem(Resource):
    def get(self, person):
        pass
    
    def put(self, person):
        pass

    def delete(self, person):
        pass

class PersonConverter(BaseConverter):
    def to_python(self, person_id):
        
        db_person = Person.query.filter_by(id=person_id).first()
        if db_person is None:
            raise NotFound
        db_person.id = str(db_person.id)
        return db_person

    def to_url(self, db_person):
        return str(db_person.id)