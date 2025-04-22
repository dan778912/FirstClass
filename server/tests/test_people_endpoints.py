import os
import sys
import pytest
from unittest.mock import patch
from http.client import NOT_ACCEPTABLE, NOT_FOUND, OK

# Add the parent directory to the path so we can import the modules
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import endpoints as ep  # noqa: E402

# Constants for endpoints
PEOPLE_EP = '/people'
MESSAGE = 'Message'
RETURN = 'Return'

TEST_CLIENT = ep.app.test_client()


@pytest.fixture
def valid_person_data():
    return {
        "name": "Test User",
        "affiliation": "Test University",
        "email": "testuser@nyu.edu",
        "role": "Student",
        "password": "testpassword123"
    }


@pytest.fixture
def existing_person_id():
    # This should be an ID that exists in the test setup
    return "delete@nyu.edu"


@patch('data.people.read', autospec=True,
       return_value={'id': {"name": 'Joe Schmoe'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(PEOPLE_EP)
    assert resp.status_code == OK or resp.status_code == 308  # Allow redirect
    if resp.status_code == 308:
        # Follow the redirect
        resp = TEST_CLIENT.get(resp.location)
        assert resp.status_code == OK

    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(person, dict)


@patch('data.people.read_one', autospec=True,
       return_value={"name": 'Joe Schmoe'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{PEOPLE_EP}/mock_id')
    assert resp.status_code == OK


@patch('data.people.read', autospec=True)
def test_get_people(mock_read):
    fake_people_data = {
        "12345": {"name": "Test User", "email": "testuser@example.com"},
        "67890": {"name": "Another User", "email": "anotheruser@example.com"}
    }

    mock_read.return_value = fake_people_data
    resp = TEST_CLIENT.get(PEOPLE_EP)

    # Handle redirect if needed
    if resp.status_code == 308:
        resp = TEST_CLIENT.get(resp.location)

    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert isinstance(person, dict)
        assert "name" in person
        assert "email" in person


def test_create_person(valid_person_data):
    with patch('data.people.create', return_value=valid_person_data):
        resp = TEST_CLIENT.post(f'{PEOPLE_EP}/create',
                                json=valid_person_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Person added!"


@pytest.mark.skip(reason="Takes too dang long")
def test_create_person_invalid_email():
    invalid_data = {
        "name": "Invalid User",
        "email": "invalid-email",
        "role": "Student",
        "password": "testpassword123"  # Add required password
    }
    resp = TEST_CLIENT.put(f'{PEOPLE_EP}/create', json=invalid_data)
    assert resp.status_code == NOT_ACCEPTABLE


def test_update_person(existing_person_id, valid_person_data):
    new_data = valid_person_data.copy()
    new_data["name"] = "Updated Name"

    with patch('data.people.update', return_value=new_data):
        resp = TEST_CLIENT.put(f'{PEOPLE_EP}/{existing_person_id}',
                               json=new_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Person updated!"


def test_get_person(existing_person_id):
    """
    tests to ensure that the correct response is given
    from the get_person endpoint.
    """
    with patch('data.people.read_one', return_value={"name": "Test User"}):
        resp = TEST_CLIENT.get(f'{PEOPLE_EP}/{existing_person_id}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "name" in resp_json


def test_del_person():
    person_id = "delete@nyu.edu"

    # Test successful deletion
    with patch('data.people.delete', return_value=1):
        resp = TEST_CLIENT.delete(f'{PEOPLE_EP}/{person_id}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "Deleted" in resp_json

    # Test person not found case - the endpoint returns 0 when person not found
    with patch('data.people.delete', return_value=0):
        resp = TEST_CLIENT.delete(f'{PEOPLE_EP}/{person_id}')
        assert resp.status_code == NOT_FOUND


@pytest.mark.skip("Skipping bc i want to mock this one.")
def test_get_masthead():
    """
    Tests to ensure that `get_masthead()` returns the right structure.
    """
    resp = TEST_CLIENT.get(f'{PEOPLE_EP}/masthead')
    resp_json = resp.get_json()

    assert resp.status_code == OK, f"Expected {OK}, got {resp.status_code}"
    assert "Masthead" in resp_json
    assert isinstance(resp_json["Masthead"], list)
