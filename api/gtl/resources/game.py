import json

from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, NotFound
from werkzeug.routing import BaseConverter

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import PlayedGame

JSON = "application/json"


class GameCollection(Resource):
    '''
    This class implements the GameCollection resource, which is a
    collection of GameItems.
    In practice, this contains all submitted games of GTL.

    Methods: GET, POST
    Path: /api/games/ 
    '''
    def get(self):
        """
        GET-method for the whole GameCollection, containing all GameItems.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all GameItems in json-form.
        Exceptions: None
        """
        body = {}
        body["items"] = []
        for db_game in PlayedGame.query.all():
            body["items"].append(db_game.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        """
        POST-method for adding new GameItems.
        Check PlayedGame.json_schema() for valid form.

        Input: None
        Output: Flask response with status 201 Created,
                containing Location-header of newly created
                resource.
        Exceptions: 415 UnsupportedMediaType
                    405 BadRequest
                    400 BadRequest
        """
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

        game = PlayedGame()
        game.deserialize(request.json)
        db.session.add(game)
        db.session.commit()

        return Response(
            status=201,
            headers={"Location": url_for("api.gameitem", game=game)},
        )


class GameItem(Resource):
    '''
    This class implements the GameItem resource.
    In practice, a single GameItem contains a submitted game of GTL.

    Methods: GET, PUT, DELETE
    Path: /api/games/<game:game>/
    '''
    def get(self, game):
        """
        GET-method for GameItem-class, used for retrieving a GameItem.

        Input: GameItem to be retrieved.
        Output: If resource found: Flask Response 200 OK,
                containing the GameItem in json-form.
                If not: 404 Not Found.
        Exceptions: None
        """
        body = game.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, game):
        """
        PUT-method for GameItem-class, used for modifying a GameItem.

        Input: GameItem to be modified.
        Output: If resource found: Flask Response 200 OK,
                containing the GameItem in json-form.
                If not: 404 Not Found.
        Exceptions: 415 UnsupportedMediaType
                    400 BadRequest
        """
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

        game.deserialize(request.json)

        db.session.commit()

        return Response(status=200)

    def delete(self, game):
        """
        DELETE-method for GameItem-class, used for deleting GameItems.

        Input: GameItem to be deleted.
        Output: If resource found: Flask Response 204 No Content,
                If not: 404 Not Found.
        Exceptions: None
        """
        print(game)
        db.session.delete(game)
        db.session.commit()

        return Response(status=204)


class GameConverter(BaseConverter):
    """
    URL converter used both in GameCollection and GameItem.
    """
    def to_python(self, game_id):
        db_game = PlayedGame.query.filter_by(id=game_id).first()
        if db_game is None:
            raise NotFound
        db_game.id = str(db_game.id)
        return db_game

    def to_url(self, db_game):
        return str(db_game.id)
