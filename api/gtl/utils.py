"""
utils.py

Contains utility functions for various things in the API.
"""

from flask import current_app
from hashids import Hashids
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from gtl.models import Location, Person, PlayedGame


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
