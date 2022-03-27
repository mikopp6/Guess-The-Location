import json

from flask import Response, url_for
from flask_restful import Resource
from gtl.models import PlayedGame
from sqlalchemy import desc

from gtl.utils import GTLBuilder

JSON = "application/json"
MASON = "application/vnd.mason+json"

class Statistic(Resource):
    '''
    This class implements the Statistic resource, which is a
    collection of GameItems sorted in different ways.

    Methods: GET
    Path: /api/statistics/ 
    '''
    def get(self):
        """
        GET-method for the whole Statistics, containing all GameItems.

        Currently only returns GameItems ordered by score in descending order.

        Input: None
        Output: Flask Response with status 200 OK,
                containing all GameItems in MASON-form.
        Exceptions: None
        """
        body = GTLBuilder()
        body.add_control(
            "alternate",
            url_for("api.gamecollection")
        )
        body["items"] = []
        for db_game in PlayedGame.query.order_by(desc("score")).all():
            item = GTLBuilder(db_game.serialize())
            item.add_control("self", url_for("api.gameitem", game=db_game))
            # item.add_control("profile", SENSOR_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)
