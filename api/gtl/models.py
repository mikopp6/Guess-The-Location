from gtl import db

class PlayedGame(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Check this https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sequences-serial-identity
    player_name = db.Column(db.String(3), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    game_type = db.Column(db.Integer)

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["player_name", "score", "timestamp"]
        }
        props = schema["properties"] = {}
        props["player_name"] = {
            "description": "3-letter name of player",
            "type": "string"
        }
        props["score"] = {
            "description": "Score of played game",
            "type": "string"
        }
        props["timestamp"] = {
            "description": "Timestamp of game completion",
            "type": "string",
        }
        return schema

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(64), nullable=False)
    country_name = db.Column(db.String(64), nullable=False)
    town_name = db.Column(db.String(64), nullable=False)

    #person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='SET NULL'))

    def serialize(self):
        return {
            "image_path": self.image_path,
            "country_name": self.country_name,
            "town_name": self.town_name
        }

    def deserialize(self, doc):
        self.image_path = doc["image_path"]
        self.country_name = doc["country_name"]
        self.town_name = doc["town_name"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["image_path", "country_name", "town_name"]
        }
        props = schema["properties"] = {}
        props["image_path"] = {
            "description": "Path to image of the location",
            "type": "string"
        }
        props["country_name"] = {
            "description": "Name of the country where location is",
            "type": "string"
        }
        props["town_name"] = {
            "description": "Name of the town/city where location is",
            "type": "string",
        }
        return schema
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    #locations = db.relationship("Location", backref='person')

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["email", "password"]
        }
        props = schema["properties"] = {}
        props["email"] = {
            "description": "Persons email address",
            "type": "string"
        }
        props["password"] = {
            "description": "Persons password",
            "type": "string"
        }
        return schema