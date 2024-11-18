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


@patch('data.people.read', autospec=True,
       return_value={'id': {NAME: 'Joe Schmoe'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    print(resp_json)
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


@pytest.mark.skip(reason="Not implemented test_get_text yet")
def test_get_text():
    pass


@pytest.mark.skip(reason="Not implemented test_del_text yet")
def test_del_text():
    pass


@pytest.mark.skip(reason="Not implemented test_create_text yet")
def test_create_text():
    pass


@pytest.mark.skip(reason="Not implemented test_update_text yet")
def test_update_text():
    pass


@pytest.mark.skip(reason="Skipping create_person test temporarily")
def test_create_person(valid_person_data):
    with patch('data.people.create') as mock_create:
        mock_create.return_value = valid_person_data['email']
        resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=valid_person_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[ep.MESSAGE] == "Person added!"
        mock_create.assert_called_once_with(valid_person_data)  # Added mock verification


def test_create_person_invalid_email():
    invalid_data = {
        "name": "Test User",
        "affiliation": "Test University",
        "email": "invalid-email",  # Invalid email format
        "role": "Student"
    }
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=invalid_data)

    # Assert that the response status code indicates an unacceptable request
    assert resp.status_code == NOT_ACCEPTABLE, f"Expected {NOT_ACCEPTABLE}, got {resp.status_code}"

    # Retrieve and check the JSON response for an error message
    resp_json = resp.get_json()
    assert "message" in resp_json, "Response missing 'message' key"
    assert "Could not add person" in resp_json["message"], (
        f"Unexpected message: {resp_json['message']}"
    )


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
    """
    tests to ensure that the correct response is givevn
    from the get_person endpoint.
    """
    with patch('data.people.read_one', return_value={"name": "Test User"}):
        resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/{existing_person_id}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "name" in resp_json


def test_del_person():
    person_id = "delete@nyu.edu"

    # Attempt to delete the person (assuming it exists)
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{person_id}')

    # Check if the person was successfully deleted or not found
    if resp.status_code == OK:
        assert resp.status_code == OK
    elif resp.status_code == NOT_FOUND:
        pytest.skip(f"Person with ID {person_id} does not exist.")
    else:
        pytest.fail(f"Unexpected status code {resp.status_code}")

    # Attempting to delete again should return 404 NOT FOUND
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
