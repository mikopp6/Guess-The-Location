import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import Location
from gtl.utils import create_hashid, decode_hashid

JSON = "application/json"


class LocationCollection(Resource):
    """
    This class implements the LocationCollection resource, which is a
    collection of LocationItems.
    In practice, this contains all locations that may be used in GTL.

    Methods: GET, POST
    Path: /api/locations/
    """

    def get(self):
        """
        GET-method for the whole LocationCollection, containing all LocationItems.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all LocationItems in json-form.
        Exceptions: None
        """
        body = {}
        body["items"] = []
        for db_location in Location.query.all():
            body["items"].append(db_location.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        """
        POST-method for adding new LocationItems.
        Check Location.json_schema() for valid form.

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
    """
    This class implements the LocationItem resource.
    In practice, a single Location contains a location for use in GTL.

    Methods: GET, PUT, DELETE
    Path: /api/locations/<location:location>/
    """

    def get(self, location):
        """
        GET-method for LocationItem-class, used for retrieving a LocationItem.

        Input: LocationItem to be retrieved.
        Output: If resource found: Flask Response 200 OK,
                containing the LocationItem in json-form.
                If not: 404 Not Found.
        Exceptions: None
        """
        body = location.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, location):
        """
        PUT-method for LocationItem-class, used for modifying a LocationItem.

        Input: LocationItem to be modified.
        Output: If resource found: Flask Response 200 OK,
                containing the LocationItem in json-form.
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

        return Response(status=204)

    def delete(self, location):
        """
        DELETE-method for LocationItem-class, used for deleting LocationItems.

        Input: LocationItem to be deleted.
        Output: If resource found: Flask Response 204 No Content,
                If not: 404 Not Found.
        Exceptions: None
        """
        db.session.delete(location)
        db.session.commit()

        return Response(status=204)


# class LocationConverter(BaseConverter):
#     """
#     URL converter used both in LocationCollection and LocationItem.
#     """

#     def to_python(self, location_id):
#         id = decode_hashid(location_id)
#         db_location = Location.query.filter_by(id=id).first()
#         if db_location is None:
#             raise NotFound
#         db_location.id = str(db_location.id)
#         return db_location

#     def to_url(self, db_location):
#         test = create_hashid(db_location.id)
#         return str(db_location.id)
