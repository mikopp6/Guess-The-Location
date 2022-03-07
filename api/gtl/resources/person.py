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
        body = {}
        body["items"] = []
        for db_person in Person.query.all():
            body["items"].append(db_person.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                Person.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            person = Person()
            person.deserialize(request.json)
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(
            status=201,
            headers={"Person": url_for("api.personitem", person=person)},
        )


class PersonItem(Resource):
    def get(self, person):
        body = person.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)
    
    def put(self, person):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                Person.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        person.deserialize(request.json)

        try:
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(status=200)

    def delete(self, person):
        db.session.delete(person)
        db.session.commit()

        return Response(status=204)

class PersonConverter(BaseConverter):
    def to_python(self, person_id):
        db_person = Person.query.filter_by(id=person_id).first()
        if db_person is None:
            raise NotFound
        db_person.id = str(db_person.id)
        return db_person

    def to_url(self, db_person):
        return str(db_person.id)