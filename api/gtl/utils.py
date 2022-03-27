"""
utils.py

Contains utility functions for various things in the API.
"""
import json
from flask import current_app, url_for, Response, request
from hashids import Hashids
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from gtl.models import Location, Person, PlayedGame

MASON = "application/vnd.mason+json"


def create_hashid(resource_id):
    """
    Create hashid by id

    Input: id
    Output: hashid
    Exceptions: None
    """
    hashids = Hashids(min_length=5, salt=current_app.config["SECRET_KEY"])
    hashid = hashids.encode(int(resource_id))
    return hashid


def decode_hashid(hashid):
    """
    Decode id by hashid

    Input: hashid
    Output: id
    Exceptions: Raises NotFound if IndexError
    """
    hashids = Hashids(min_length=5, salt=current_app.config["SECRET_KEY"])
    resource_id = hashids.decode(hashid)
    try:
        fixed_id = resource_id[0]
    except IndexError as error:
        raise NotFound("Not found by ID") from error
    return fixed_id


class LocationConverter(BaseConverter):
    """
    URL converter used both in LocationCollection and LocationItem.
    """

    def to_python(self, value):
        resource_id = decode_hashid(value)
        db_location = Location.query.filter_by(id=resource_id).first()
        if db_location is None:
            raise NotFound
        db_location.id = str(db_location.id)
        return db_location

    def to_url(self, value):
        resource_id = create_hashid(value.id)
        return str(resource_id)


class PersonConverter(BaseConverter):
    """
    URL converter used both in PersonCollection and PersonItem.
    """

    def to_python(self, value):
        resource_id = decode_hashid(value)
        db_person = Person.query.filter_by(id=resource_id).first()
        if db_person is None:
            raise NotFound
        db_person.id = str(db_person.id)
        return db_person

    def to_url(self, value):
        resource_id = create_hashid(value.id)
        return str(resource_id)


class GameConverter(BaseConverter):
    """
    URL converter used both in GameCollection and GameItem.
    """

    def to_python(self, value):
        resource_id = decode_hashid(value)
        db_game = PlayedGame.query.filter_by(id=resource_id).first()
        if db_game is None:
            raise NotFound
        db_game.id = str(db_game.id)
        return db_game

    def to_url(self, value):
        resource_id = create_hashid(value.id)
        return str(resource_id)


class MasonBuilder(dict):
    """
    MasonBuilder is based on course material:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-3-api-documentation-and-hypermedia

    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.

    Note that child classes should set the *DELETE_RELATION* to the application
    specific relation name from the application namespace. The IANA standard
    does not define a link relation for deleting something.
    """

    DELETE_RELATION = ""

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, namespace, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][namespace] = {"name": uri}

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_control_post(self, ctrl_name, title, href, schema):
        """
        Utility method for adding POST type controls. The control is
        constructed from the method's parameters. Method and encoding are
        fixed to "POST" and "json" respectively.

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            ctrl_name, href, method="POST", encoding="json", title=title, schema=schema
        )

    def add_control_put(self, title, href, schema):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control name, method and
        encoding are fixed to "edit", "PUT" and "json" respectively.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            "edit", href, method="PUT", encoding="json", title=title, schema=schema
        )

    def add_control_delete(self, ctrl_name, title, href):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control method is fixed to
        "DELETE", and control's name is read from the class attribute
        *DELETE_RELATION* which needs to be overridden by the child class.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        """

        self.add_control(
            ctrl_name,
            href,
            method="DELETE",
            title=title,
        )


class GTLBuilder(MasonBuilder):
    """
    GameBuilder is based on course material:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-3-api-documentation-and-hypermedia

    Using MasonBuilder, GameBuilder enables adding hypermedia controls
    for the GameItem and GameCollection resources.

    """

    def add_control_add_game(self):
        """
        Using MasonBuilder, adds hypermedia link to a response for adding a game.
        """
        self.add_control_post(
            "gtl:add-game",
            "Create a new game",
            url_for("api.gamecollection"),
            PlayedGame.json_schema(),
        )

    def add_control_delete_game(self, game):
        """
        Using MasonBuilder, adds hypermedia link to a response for deleting a game.
        """
        self.add_control_delete(
            "gtl:delete", "Delete this game", url_for("api.gameitem", game=game)
        )

    def add_control_modify_game(self, game):
        """
        Using MasonBuilder, adds hypermedia link to a response for modifying a game.
        """
        self.add_control_put(
            "Update this game",
            url_for("api.gameitem", game=game),
            PlayedGame.json_schema(),
        )

    def add_control_add_location(self):
        """
        Using MasonBuilder, adds hypermedia link to a response for adding a location.
        """
        self.add_control_post(
            "gtl:add-location",
            "Create a new location",
            url_for("api.locationcollection"),
            Location.json_schema(),
        )

    def add_control_delete_location(self, location):
        """
        Using MasonBuilder, adds hypermedia link to a response for deleting a location.
        """
        self.add_control_delete(
            "gtl:delete",
            "Delete this location",
            url_for("api.locationitem", location=location),
        )

    def add_control_modify_location(self, location):
        """
        Using MasonBuilder, adds hypermedia link to a response for modifying a location.
        """
        self.add_control_put(
            "Update this location",
            url_for("api.locationitem", location=location),
            Person.json_schema(),
        )

    def add_control_add_person(self):
        """
        Using MasonBuilder, adds hypermedia link to a response for adding a person.
        """
        self.add_control_post(
            "gtl:add-person",
            "Create a new person",
            url_for("api.personcollection"),
            Person.json_schema(),
        )

    def add_control_delete_person(self, person):
        """
        Using MasonBuilder, adds hypermedia link to a response for deleting a person.
        """
        self.add_control_delete(
            "gtl:delete", "Delete this person", url_for("api.personitem", person=person)
        )

    def add_control_modify_person(self, person):
        """
        Using MasonBuilder, adds hypermedia link to a response for modifying a person.
        """
        self.add_control_put(
            "Update this person",
            url_for("api.personitem", person=person),
            Person.json_schema(),
        )


def create_error_response(status_code, title, message=None):
    """
    create_error_response is based on course material:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-3-api-documentation-and-hypermedia

    Used to create uniform error responses.

    Input: status_code: HTTP Status code
            title: Title of error response
            message: Error message
    Output: Returns formatted MASON error response
    Exceptions: None
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    # body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)
