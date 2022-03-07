import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict, NotFound
from werkzeug.routing import BaseConverter

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import Location


JSON = "application/json"


class LocationCollection(Resource):
    def get(self):
        body = {}
        body["items"] = []
        for db_location in Location.query.all():
            body["items"].append(db_location.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                Location.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            location = Location()
            location.deserialize(request.json)
            db.session.add(location)
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(
            status=201,
            headers={"Location": url_for("api.locationitem", location=location)},
        )


class LocationItem(Resource):
    def get(self, location):
        body = location.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, location):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                Location.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        location.deserialize(request.json)

        try:
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(status=200)

    def delete(self, location):
        db.session.delete(location)
        db.session.commit()

        return Response(status=204)


class LocationConverter(BaseConverter):
    def to_python(self, location_id):

        db_location = Location.query.filter_by(id=location_id).first()
        if db_location is None:
            raise NotFound
        db_location.id = str(db_location.id)
        return db_location

    def to_url(self, db_location):
        return str(db_location.id)
