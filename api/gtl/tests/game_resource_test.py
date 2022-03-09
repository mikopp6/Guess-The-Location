import json
import os
from random import randint
import pytest
import tempfile
import datetime

from gtl.models import PlayedGame
from gtl import create_app, db

# based on http://flask.pocoo.org/docs/1.0/testing/
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {"SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname, "TESTING": True}

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()

    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)


def _populate_db():
    names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ"]
    for i in range(0, 10):
        s = PlayedGame(
            player_name=names[i],
            score=(100*(i+1)),
            timestamp=datetime.datetime.utcnow(),
            game_type=randint(0, 3)
        )
        db.session.add(s)
    db.session.commit()

def _get_game_json():
    """
    Creates a valid game JSON object to be used for PUT and POST tests.
    """

    return {
        "player_name": "MIK",
        "score": 123001,
        "timestamp": str(datetime.datetime.utcnow()),
        "game_type": 1,
    }

class TestGameCollection(object):
    """
    This class implements tests for each HTTP method in the games collection
    resource.
    """

    RESOURCE_URL = "/api/games/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that the number of items is correct, and that all of the 
        expected attributes are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 10
        for item in body["items"]:
            assert "player_name" in item
            assert "score" in item
            assert "timestamp" in item
            assert "game_type" in item
    
    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and
        also checks that a valid request receives a 201 response with a
        location header that leads into the newly created resource.
        Checks that all attributes are present in this new resource. 
        """

        valid = _get_game_json()
        valid_object_id = "11"
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid_object_id + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["player_name"] == "MIK"
        assert body["score"] == 123001
        # assert body["timestamp"] == time ??, idk not necessary to test this
        assert body["game_type"] == 1

        # remove imagepath field for 400
        valid.pop("player_name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
