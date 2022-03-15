import os
import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# Based on course example https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/flask-api-project-layout/,
# which is based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory


def create_app(test_config=None):
    """
    Main Flask app used to serve the api.

    Input: test_config, used when testing. Defaults to None
    Output: Flask app
    Exceptions: None
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "gtl_dev.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
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

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_test_data)

    from gtl.resources.location import LocationConverter
    from gtl.resources.game import GameConverter
    from gtl.resources.person import PersonConverter

    app.url_map.converters["location"] = LocationConverter
    app.url_map.converters["game"] = GameConverter
    app.url_map.converters["person"] = PersonConverter

    app.register_blueprint(api.api_bp)

    migrate = Migrate(app, db)
    return app
