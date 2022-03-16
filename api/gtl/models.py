"""
models.py

All necessary resource classes are defined here,
and the populations scripts needed in development.
"""
import datetime
import click
from flask.cli import with_appcontext

from gtl import db

class PlayedGame(db.Model):
    """
    This class is for a single game of GTL.
    Used primarily in resources/game.py
    and statistic.py
    """

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(3), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    game_type = db.Column(db.Integer)

    def serialize(self):
        """
        Serializes PlayedGame. Needed in GET-methods.

        Input: None
        Output: Serialized version of PlayedGame
        Exceptions: None
        """
        return {
            "player_name": self.player_name,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
            "game_type": self.game_type,
        }

    def deserialize(self, doc):
        """
        Deserializes PlayedGame. For use in POST and PUT -methods.

        Input: doc: serialized PlayedGame
        Output: None
        Exceptions: None
        """
        self.player_name = doc["player_name"]
        self.score = doc["score"]
        self.timestamp = datetime.datetime.fromisoformat(doc["timestamp"])
        self.game_type = doc["game_type"]

    @staticmethod
    def json_schema():
        """
        Defines the json schema of PlayedGame.
        Used for validation in POST and PUT methods.
        """
        schema = {"type": "object", "required": ["player_name", "score"]}
        props = schema["properties"] = {}
        props["player_name"] = {
            "description": "3-letter name of player",
            "type": "string",
            "maxLength": 3,
        }
        props["score"] = {"description": "Score of played game", "type": "number"}
        props["timestamp"] = {
            "description": "Timestamp of game completion",
            "type": "string",
            "pattern": r"^\d{4}-[01]\d-[0-3]\d?[T ][0-2]\d:[0-5]\d:[0-5]\d(?:\.\d+)?$",
        }
        return schema


class Location(db.Model):
    """
    This class is for a single location in GTL.
    Used primarily in resources/location.py
    """

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(64), unique=True, nullable=False)
    country_name = db.Column(db.String(64), nullable=False)
    town_name = db.Column(db.String(64), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="SET NULL"))
    person = db.relationship("Person", back_populates="locations")

    def serialize(self):
        """
        Serializes Location. Needed in GET-methods.

        Input: None
        Output: Serialized version of Location
        Exceptions: None
        """
        return {
            "image_path": self.image_path,
            "country_name": self.country_name,
            "town_name": self.town_name,
            "person_id": self.person_id,
        }

    def deserialize(self, doc):
        """
        Deserializes Location. For use in POST and PUT -methods.

        Input: doc: serialized Location
        Output: None
        Exceptions: None
        """
        self.image_path = doc["image_path"]
        self.country_name = doc["country_name"]
        self.town_name = doc["town_name"]
        self.person_id = doc["person_id"]

    @staticmethod
    def json_schema():
        """
        Defines the json schema of Location.
        Used for validation in POST and PUT methods.
        """
        schema = {
            "type": "object",
            "required": ["image_path", "country_name", "town_name"],
        }
        props = schema["properties"] = {}
        props["image_path"] = {
            "description": "Unique path to image of the location",
            "type": "string",
        }
        props["country_name"] = {
            "description": "Name of the country where location is",
            "type": "string",
        }
        props["town_name"] = {
            "description": "Name of the town/city where location is",
            "type": "string",
        }
        return schema


class Person(db.Model):
    """
    This class is for a single person in GTL.
    Used primarily in resources/person.py
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    locations = db.relationship("Location", back_populates="person")

    def serialize(self):
        """
        Serializes Person, and their Locations. Needed in GET-methods.

        Input: None
        Output: Serialized version of Person
        Exceptions: None
        """
        locations = []
        if self.locations:
            for location in self.locations:
                locations.append(location.serialize())
        return {"email": self.email, "password": self.password, "locations": locations}

    def deserialize(self, doc):
        """
        Deserializes Person. For use in POST and PUT -methods.

        Input: doc: serialized Person
        Output: None
        Exceptions: None
        """
        self.email = doc["email"]
        self.password = doc["password"]

    @staticmethod
    def json_schema():
        """
        Defines the json schema of Person.
        Used for validation in POST and PUT methods.
        """
        schema = {"type": "object", "required": ["email", "password"]}
        props = schema["properties"] = {}
        props["email"] = {"description": "Persons email address", "type": "string"}
        props["password"] = {"description": "Persons password", "type": "string"}
        return schema


@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Create database. Used with "Flask init-db"
    """
    db.create_all()
    print("Database created")


@click.command("testgen")
@with_appcontext
def generate_test_data():
    """
    Populates db with test data
    """
    from random import randint
    import json

    persons = [
        {"email": "thisismy@email.com", "password": "exampleofastrongpasswordthisisnt"},
        {
            "email": "thisisnotmy@email.com",
            "password": "exampleofanevenstrongerpasswordthisisnt",
        },
        {
            "email": "thisusedtobemy@email.com",
            "password": "exampleofthestrongestpasswordintheworldthisisnt",
        },
    ]
    # List names
    names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ"]
    # List of played games
    games = []
    # Generate list of games from names
    for name in names:
        games.append(
            {
                "player_name": name,
                "score": randint(0, 10000),
                "timestamp": datetime.datetime.utcnow(),
                "game_type": randint(0, 3),
            }
        )
    # Add persons to db session
    for person in persons:
        person = Person(
            email=person["email"],
            password=person["password"],
        )
        db.session.add(person)
    # Add locations to db session
    with open("static/locationdata.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for location in data["locations"]:
            location = Location(
                image_path=location["image_path"],
                country_name=location["country_name"],
                town_name=location["town_name"],
                person_id=location["person_id"],
            )
            db.session.add(location)
    # Add played games to db session
    for game in games:
        played_game = PlayedGame(
            player_name=game["player_name"],
            score=game["score"],
            timestamp=game["timestamp"],
            game_type=game["game_type"],
        )
        db.session.add(played_game)
    # Commit persons, locations and games
    db.session.commit()
    print("Data generated")
