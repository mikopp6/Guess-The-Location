from tracemalloc import Statistic
from flask import Blueprint
from flask_restful import Api

from gtl.resources.location import LocationCollection, LocationItem
from gtl.resources.game import GameCollection, GameItem
from gtl.resources.person import PersonCollection, PersonItem
from gtl.resources.statistic import Statistic

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(LocationCollection, "/locations/")
api.add_resource(LocationItem, "/locations/<location:location>/")
api.add_resource(PersonCollection, "/persons/")
api.add_resource(PersonItem, "/persons/<person:person>/")
api.add_resource(GameCollection, "/games/")
api.add_resource(GameItem, "/games/<game:game>/")
api.add_resource(Statistic, "/statistics/")
