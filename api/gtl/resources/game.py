import json
from sqlalchemy.exc import IntegrityError

from flask import Response, request, url_for
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict, NotFound
from werkzeug.routing import BaseConverter

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import PlayedGame
from datetime import datetime

JSON = "application/json"


class GameCollection(Resource):
    def get(self):
        body = {}
        body["items"] = []
        for db_game in PlayedGame.query.all():
            body["items"].append(db_game.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                PlayedGame.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        try:
            game = PlayedGame(
                player_name=request.json["player_name"],
                score=request.json["score"],
                timestamp=datetime.now(),
                game_type=request.json["game_type"],
            )
            db.session.add(game)
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(
            status=201,
            headers={"Game": url_for("api.gameitem", game=game)},
        )


class GameItem(Resource):
    def get(self, game):
        body = game.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, game):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(
                request.json,
                PlayedGame.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            raise BadRequest(description=str(e))

        game.player_name = request.json["player_name"]
        game.score = request.json["score"]
        game.game_type = request.json["game_type"]

        try:
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Already exists")

        return Response(status=200)

    def delete(self, game):
        db.session.delete(game)
        db.session.commit()

        return Response(status=204)


class GameConverter(BaseConverter):
    def to_python(self, game_id):
        print("testii")
        db_game = PlayedGame.query.filter_by(id=game_id).first()
        if db_game is None:
            raise NotFound
        db_game.id = str(db_game.id)
        return db_game

    def to_url(self, db_game):
        return str(db_game.id)
