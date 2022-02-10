from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "" # INSERT POSTGRESQL HERE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class PlayedGame(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Check this https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sequences-serial-identity
    playerName = db.Column(db.String(3), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)
    gameType = db.Column(db.Integer)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagePath = db.Column(db.String(64), nullable=False)
    countryName = db.Column(db.String(64), nullable=False)
    townName = db.Column(db.String(64), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)


    
