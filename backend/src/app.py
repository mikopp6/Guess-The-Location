from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig, ProductionConfig
from models import PlayedGame, Location, User

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

