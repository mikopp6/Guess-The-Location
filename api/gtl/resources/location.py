import json

from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Conflict, NotFound
from werkzeug.routing import BaseConverter

from gtl.models import *


JSON = "application/json"

class LocationCollection(Resource):

    def get(self):
        pass


    def post(self):
        pass

class LocationItem(Resource):
    def get(self, location):
        body = location.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)
    
    def put(self, location):
        pass

    def delete(self, location):
        pass

class LocationConverter(BaseConverter):
    def to_python(self, location_id):
        
        db_location = Location.query.filter_by(id=location_id).first()
        if db_location is None:
            raise NotFound
        db_location.id = str(db_location.id)
        print("in convert")
        return db_location

    def to_url(self, db_location):
        return db_location.id