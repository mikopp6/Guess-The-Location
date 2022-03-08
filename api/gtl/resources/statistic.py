import json

from flask import Response
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from gtl.models import PlayedGame
from sqlalchemy import desc

JSON = "application/json"


class Statistic(Resource):
    def get(self):
        body = {}
        body["items"] = []
        for db_game in PlayedGame.query.order_by(desc("score")).all():
            body["items"].append(db_game.serialize())

        return Response(json.dumps(body), 200, mimetype=JSON)
