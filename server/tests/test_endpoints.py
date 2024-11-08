from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

from data.people import NAME

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


@pytest.fixture
def valid_person_data():
    return {
        "name": "Test User",
        "affiliation": "Test University",
        "email": "testuser@nyu.edu",
        "role": "Student"
    }

@pytest.fixture
def existing_person_id():
    # This should be an ID that exists in the test setup
    return "delete@nyu.edu"


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)


def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    print(resp_json)
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


@pytest.mark.skip(reason="Skipping get_people test temporarily")
def test_create_person(valid_person_data):
    with patch('data.people.create') as mock_create:
        mock_create.return_value = valid_person_data['email']
        resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=valid_person_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[ep.MESSAGE] == "Person added!"


def test_create_person_invalid_email():
    invalid_data = {
        "name": "Test User",
        "affiliation": "Test University",
        "email": "invalid-email",  # Invalid email format
        "role": "Student"
    }
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=invalid_data)
    
    assert resp.status_code == NOT_ACCEPTABLE
    
    resp_json = resp.get_json()
    print("Response JSON for invalid email test:", resp_json)  # Debugging output
    
    # Adjusted to match lowercase 'message' in the actual response
    assert "message" in resp_json, "Response missing 'message' key"
    assert "Could not add person" in resp_json["message"]


def test_update_person(existing_person_id, valid_person_data):
    new_data = valid_person_data.copy()
    new_data["name"] = "Updated Name"
    with patch('data.people.update') as mock_update:
        mock_update.return_value = new_data
        resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/update/{existing_person_id}', json=new_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[ep.MESSAGE] == "Person updated!"


def test_get_person(existing_person_id):
    with patch('data.people.read_one', return_value={"name": "Test User"}):
        resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/{existing_person_id}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "name" in resp_json


def test_del_person():
    """
    tests to ensure that successful status codes are received if
    person is successfully deleted. otherwise should return a 404 status code
    """

    person_id = "delete@nyu.edu"

    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{person_id}')
    assert resp.status_code == OK

    double_delete_resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{person_id}')
    assert double_delete_resp.status_code == NOT_FOUND


def test_get_masthead():
    """
    Tests to ensure that `get_masthead()` returns the right structure.
    """
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/masthead')
    resp_json = resp.get_json()

    assert resp.status_code == OK, f"Expected {OK}, got {resp.status_code}"
    assert ep.MASTHEAD in resp_json, "Response missing expected 'Masthead' key"
    assert isinstance(resp_json[ep.MASTHEAD], dict), (
        "Expected 'Masthead' value to be a dictionary"
        )
