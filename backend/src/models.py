from app import db

class PlayedGame(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Check this https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sequences-serial-identity
    player_name = db.Column(db.String(3), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    game_type = db.Column(db.Integer)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(64), nullable=False)
    country_name = db.Column(db.String(64), nullable=False)
    town_name = db.Column(db.String(64), nullable=False)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
