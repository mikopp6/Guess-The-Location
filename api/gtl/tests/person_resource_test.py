import json
import os
import pytest
import tempfile

from gtl.models import Location, Person
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
        s = Person(email="user{}@gmail.com".format(i), password="hunter{}".format(i))
        db.session.add(s)

    for i in range(0, 8):
        s = Location(
            image_path="testikuva{}.jpg".format(i),
            country_name="country{}".format(i),
            town_name="town{}".format(i),
            person_id=(i % 3) + 1,
        )
        print(s.person_id)
        db.session.add(s)

    db.session.commit()


def _get_person_json():
    """
    Creates a valid person JSON object to be used for PUT and POST tests.
    """

    return {"email": "testi@testi.com", "password": "testi123"}


class TestPersonCollection(object):
    """
    This class implements tests for each HTTP method in the person collection
    resource.
    """

    RESOURCE_URL = "/api/persons/"

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
        for index, item in enumerate(body["items"]):
            assert "email" in item
            assert "password" in item
            assert "locations" in item
            if index == 1:
                assert len(item["locations"]) == 3
            if index == 2:
                assert len(item["locations"]) == 2

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and
        also checks that a valid request receives a 201 response with a
        person header that leads into the newly created resource.
        Checks that all attributes are present in this new resource.
        """

        valid = _get_person_json()
        valid_object_id = "p7olP"

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(
            self.RESOURCE_URL + valid_object_id + "/"
        )
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["email"] == "testi@testi.com"
        assert body["password"] == "testi123"

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove email field for 400
        valid.pop("email")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestPersonItem(object):

    RESOURCE_URL = "/api/persons/G73a9/"
    LOCATIONS_RESOURCE_URL = "/api/locations/G73a9/"
    INVALID_URL = "/api/persons/x/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes are present.
        Also checks that an invalid url returns 404.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["email"] == "user0@gmail.com"
        assert body["password"] == "hunter0"

        # test invalid url
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response.
        """

        valid = _get_person_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test invalid url
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another person's email
        valid["email"] = "user2@gmail.com"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid (only change password)
        valid["email"] = "user99@gmail.com"
        valid["password"] = "newpw"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("password")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request receives 204
        response and that trying to GET the person afterwards results in 404.
        Also checks that trying to delete a person that doesn't exist results
        in 404.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

        # check that location associated had its person set to null
        resp = client.get(self.LOCATIONS_RESOURCE_URL)
        body = json.loads(resp.data)
        assert not body["person_id"]
