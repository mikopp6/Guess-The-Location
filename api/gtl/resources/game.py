import json

from flask import Response, request, url_for
from flask_restful import Resource

from jsonschema import validate, ValidationError, draft7_format_checker

from gtl import db
from gtl.models import PlayedGame
from gtl.utils import GTLBuilder, create_error_response

JSON = "application/json"
MASON = "application/vnd.mason+json"

class GameCollection(Resource):
    """
    This class implements the GameCollection resource, which is a
    collection of GameItems.
    In practice, this contains all submitted games of GTL.

    Methods: GET, POST
    Path: /api/games/
    """

    def get(self):
        """
        GET-method for the whole GameCollection, containing all GameItems.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all GameItems in MASON-form.
        Exceptions: None
        """

        body = GTLBuilder()
        body.add_namespace("gtl", "/api/link-relations/")
        body.add_control("self", url_for("api.gamecollection"))
        body.add_control_add_game()
        body.add_control("locations-all", url_for("api.locationcollection"))
        body.add_control("persons-all", url_for("api.personcollection"))
        body.add_control(
            "alternate",
            url_for("api.statistic"),
            description="Gamecollection sorted by score, in descending order",
        )
        body["items"] = []
        for db_game in PlayedGame.query.all():
            item = GTLBuilder(db_game.serialize())
            item.add_control("self", url_for("api.gameitem", game=db_game))
            # item.add_control("profile", GAME_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

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
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )
        try:
            validate(
                request.json,
                PlayedGame.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:        
            return create_error_response(400, "Invalid JSON document", str(e))

        game = PlayedGame()
        game.deserialize(request.json)
        db.session.add(game)
        db.session.commit()

        return Response(
            status=201,
            headers={"Location": url_for("api.gameitem", game=game)},
        )


class GameItem(Resource):
    """
    This class implements the GameItem resource.
    In practice, a single GameItem contains a submitted game of GTL.

    Methods: GET, PUT, DELETE
    Path: /api/games/<game:game>/
    """

    def get(self, game):
        """
        GET-method for GameItem-class, used for retrieving a GameItem.

        Input: GameItem to be retrieved.
        Output: If resource found: Flask Response 200 OK,
                containing the GameItem in MASON-form.
                If not: 404 Not Found.
        Exceptions: None
        """
        body = GTLBuilder(game.serialize())
        body.add_namespace("gtl", "/api/link-relations/")
        body.add_control("self", url_for("api.gameitem", game=game))
        # body.add_control("profile", SENSOR_PROFILE)
        body.add_control("collection", url_for("api.gamecollection"))
        body.add_control_delete_game(game)
        body.add_control_modify_game(game)

        return Response(json.dumps(body), 200, mimetype=MASON)

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
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(
                request.json,
                PlayedGame.json_schema(),
                format_checker=draft7_format_checker,
            )
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        game.deserialize(request.json)
        db.session.commit()

        return Response(status=204)

    def delete(self, game):
        """
        DELETE-method for GameItem-class, used for deleting GameItems.

        Input: GameItem to be deleted.
        Output: If resource found: Flask Response 204 No Content,
                If not: 404 Not Found.
        Exceptions: None
        """
        db.session.delete(game)
        db.session.commit()

        return Response(status=204)
