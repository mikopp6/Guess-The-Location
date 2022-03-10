import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict, NotFound
from werkzeug.routing import BaseConverter

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import Person

JSON = "application/json"

class PersonCollection(Resource):
    '''
    This class implements the PersonCollection resource, which is a
    collection of PersonItems.
    In practice, this contains all persons that may be used in GTL.

    Methods: GET, POST
    Path: /api/persons/ 
    '''
    def get(self):
        """
        GET-method for the whole PersonCollection, containing all PersonItems.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all PersonItems in json-form.
        Exceptions: None
        """
        body = {}
        body["items"] = []
        for db_person in Person.query.all():
            body["items"].append(db_person.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        """
        POST-method for adding new PersonItems.
        Check Person.json_schema() for valid form.

        Input: None
        Output: Flask response with status 201 Created,
                containing Location-header of newly created
                resource.
        Exceptions: 415 UnsupportedMediaType
                    405 BadRequest
                    400 BadRequest
                    409 Conflict
        """
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
            headers={"Location": url_for("api.personitem", person=person)},
        )


class PersonItem(Resource):
    '''
    This class implements the PersonItem resource.
    In practice, a single Persons contains a person for use in GTL.

    Methods: GET, PUT, DELETE
    Path: /api/persons/<person:person>/
    '''
    def get(self, person):
        """
        GET-method for PersonItem-class, used for retrieving a PersonItem.

        Input: PersonItem to be retrieved.
        Output: If resource found: Flask Response 200 OK,
                containing the PersonItem in json-form.
                If not: 404 Not Found.
        Exceptions: None
        """
        body = person.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)
    
    def put(self, person):
        """
        PUT-method for PersonItem-class, used for modifying a PersonItem.

        Input: PersonItem to be modified.
        Output: If resource found: Flask Response 200 OK,
                containing the PersonItem in json-form.
                If not: 404 Not Found.
        Exceptions: 415 UnsupportedMediaType
                    400 BadRequest
                    409 Conflict
        """
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
        """
        DELETE-method for PersonItem-class, used for deleting PersonItems.

        Input: PersonItem to be deleted.
        Output: If resource found: Flask Response 204 No Content,
                If not: 404 Not Found.
        Exceptions: None
        """
        db.session.delete(person)
        db.session.commit()

        return Response(status=204)

class PersonConverter(BaseConverter):
    """
    URL converter used both in PersonCollection and PersonItem.
    """
    def to_python(self, person_id):
        db_person = Person.query.filter_by(id=person_id).first()
        if db_person is None:
            raise NotFound
        db_person.id = str(db_person.id)
        return db_person

    def to_url(self, db_person):
        return str(db_person.id)