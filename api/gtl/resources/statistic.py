import json

from flask import Response
from flask_restful import Resource
from gtl.models import PlayedGame
from sqlalchemy import desc

JSON = "application/json"

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
                containing all GameItems in json-form.
        Exceptions: None
        """
        body = {}
        body["items"] = []
        for db_game in PlayedGame.query.order_by(desc("score")).all():
            body["items"].append(db_game.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)
