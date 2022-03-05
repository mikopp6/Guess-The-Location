import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Based on course example https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/flask-api-project-layout/,
# which is based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "",
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/gtl_dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)

    from . import models
    from . import api
    from gtl.resources.location import LocationConverter
    app.url_map.converters["location"] = LocationConverter
    
    app.register_blueprint(api.api_bp)

    return app