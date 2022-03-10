import json
import os
import pytest
import tempfile

from gtl.models import Location
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
    for i in range(0, 4):
        s = Location(
            image_path="testikuva{}.jpg".format(i),
            country_name="country{}".format(i),
            town_name="town{}".format(i),
            person_id=1,
        )
        db.session.add(s)
    db.session.commit()


def _get_location_json():
    """
    Creates a valid location JSON object to be used for PUT and POST tests.
    """

    return {
        "image_path": "testi.jpg",
        "country_name": "Finland",
        "town_name": "Oulu",
        "person_id": 1,
    }


class TestLocationCollection(object):
    """
    This class implements tests for each HTTP method in the location collection
    resource.
    """

    RESOURCE_URL = "/api/locations/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that the number of items is correct, and that all of the 
        expected attributes are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body["items"]) == 4
        for item in body["items"]:
            assert "image_path" in item
            assert "country_name" in item
            assert "town_name" in item
            assert "person_id" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and
        also checks that a valid request receives a 201 response with a
        location header that leads into the newly created resource.
        Checks that all attributes are present in this new resource.
        """

        valid = _get_location_json()
        valid_object_id = "5"

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
        assert body["image_path"] == "testi.jpg"
        assert body["country_name"] == "Finland"
        assert body["town_name"] == "Oulu"
        assert body["person_id"] == 1

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove imagepath field for 400
        valid.pop("image_path")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestLocationItem(object):

    RESOURCE_URL = "/api/locations/1/"
    INVALID_URL = "/api/locations/x/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes are present.
        Also checks that an invalid url returns 404.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["image_path"] == "testikuva0.jpg"
        assert body["country_name"] == "country0"
        assert body["town_name"] == "town0"
        assert body["person_id"] == 1
        
        # test invalid url
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response.
        """

        valid = _get_location_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test invalid url
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another location's name
        valid["image_path"] = "testikuva1.jpg"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid (only change countryname)
        valid["image_path"] = "testikuva0.jpg"
        valid["country_name"] = "sweden"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200

        # remove field for 400
        valid.pop("country_name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request receives 204
        response and that trying to GET the location afterwards results in 404.
        Also checks that trying to delete a location that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
