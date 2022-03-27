import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import Person, Location
from gtl.utils import GTLBuilder, create_error_response

JSON = "application/json"
MASON = "application/vnd.mason+json"


class PersonCollection(Resource):
    """
    This class implements the PersonCollection resource, which is a
    collection of PersonItems.
    In practice, this contains all persons that may be used in GTL.

    Methods: GET, POST
    Path: /api/persons/
    """

    def get(self):
        """
        GET-method for the whole PersonCollection, containing all PersonItems.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all PersonItems in MASON-form.
        Exceptions: None
        """
        body = GTLBuilder()
        body.add_namespace("gtl", "/api/link-relations/")
        body.add_control("self", url_for("api.personcollection"))
        body.add_control_add_person()
        body.add_control("locations-all", url_for("api.locationcollection"))
        body.add_control("games-all", url_for("api.gamecollection"))
        body["items"] = []
        for db_person in Person.query.all():
            item = GTLBuilder(db_person.serialize())
            item.add_control("self", url_for("api.personitem", person=db_person))
            # item.add_control("profile", PERSON_PROFILE)
            for index, db_location in enumerate(item["locations"]):
                db_location = Location.query.filter_by(image_path=db_location["image_path"]).first()
                inside_item = GTLBuilder(db_location.serialize())
                inside_item.add_control("self", url_for("api.locationitem", location=db_location))
                # item.add_control("profile", LOCATION_PROFILE)
                item["locations"][index] = inside_item
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

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
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )
        try:
            validate(
                request.json,
                Person.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        try:
            person = Person()
            person.deserialize(request.json)
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists")

        return Response(
            status=201,
            headers={"Location": url_for("api.personitem", person=person)},
        )


class PersonItem(Resource):
    """
    This class implements the PersonItem resource.
    In practice, a single Persons contains a person for use in GTL.

    Methods: GET, PUT, DELETE
    Path: /api/persons/<person:person>/
    """

    def get(self, person):
        """
        GET-method for PersonItem-class, used for retrieving a PersonItem.

        Input: PersonItem to be retrieved.
        Output: If resource found: Flask Response 200 OK,
                containing the PersonItem in MASON-form.
                If not: 404 Not Found.
        Exceptions: None
        """
        body = GTLBuilder(person.serialize())
        body.add_namespace("gtl", "/api/link-relations/")
        body.add_control("self", url_for("api.personitem", person=person))
        # body.add_control("profile", SENSOR_PROFILE)
        body.add_control("collection", url_for("api.personcollection"))
        body.add_control_delete_person(person)
        body.add_control_modify_person(person)
        for index, db_location in enumerate(body["locations"]):
                db_location = Location.query.filter_by(image_path=db_location["image_path"]).first()
                inside_item = GTLBuilder(db_location.serialize())
                inside_item.add_control("self", url_for("api.locationitem", location=db_location))
                # item.add_control("profile", LOCATION_PROFILE)
                body["locations"][index] = inside_item
        return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, person):
        """
        PUT-method for PersonItem-class, used for modifying a PersonItem.

        Input: PersonItem to be modified.
        Output: If resource found: Flask Response 204 OK,
                containing the PersonItem in json-form.
                If not: 404 Not Found.
        Exceptions: 415 UnsupportedMediaType
                    400 BadRequest
                    409 Conflict
        """
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(
                request.json,
                Person.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        person.deserialize(request.json)

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists")

        return Response(status=204)

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
