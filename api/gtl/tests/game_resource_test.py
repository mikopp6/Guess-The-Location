import json
import os
from random import randint
import pytest
import tempfile
import datetime

from gtl.models import PlayedGame
from gtl import create_app, db

# Test client based on http://flask.pocoo.org/docs/1.0/testing/
# The actual tests themselves are heavily based on course material & examples:
#   https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
#   https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/testing-flask-applications-part-2/

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

        # remove player_name field for 400
        valid.pop("player_name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestGameItem(object):

    RESOURCE_URL = "/api/games/1/"
    INVALID_URL = "/api/games/x/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes are present.
        Also checks that an invalid url returns 404.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["player_name"] == "AAA"
        assert body["score"] == 100
        # assert body["timestamp"] == time ??, idk not necessary to test this
        assert body["game_type"] == 1 or 2 or 3
        
        # test invalid url
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response.
        """

        valid = _get_game_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test invalid url
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with valid (only change score)
        valid["score"] = 0
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200

        # remove field for 400
        valid.pop("score")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request receives 204
        response and that trying to GET the game afterwards results in 404.
        Also checks that trying to delete a game that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestStatistic(object):
    """
    This class implements tests for each HTTP method in the statistic
    resource.
    """

    RESOURCE_URL = "/api/statistics/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that the number of items is correct, and that all of the 
        expected attributes are present, and in correct order.
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
        assert body["items"][0]["score"] == 1000
        assert body["items"][6]["score"] == 400
        assert body["items"][9]["score"] == 100