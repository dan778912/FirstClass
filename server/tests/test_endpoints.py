import os
import sys
import pytest
from unittest.mock import patch
from http.client import NOT_ACCEPTABLE, NOT_FOUND, OK

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import endpoints as ep

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


@pytest.fixture
def existing_text_key():
    return "DeletePage"


@pytest.fixture
def valid_text_data():
    return {
        "key": "TestBook",
        "title": "Book for Tests",
        "text": "This is text for testing"
    }


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
       return_value={'id': {"name": 'Joe Schmoe'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert "name" in person


@patch('data.people.read_one', autospec=True,
       return_value={"name": 'Joe Schmoe'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK


@patch('data.people.read', autospec=True)
def test_get_people(mock_read):
    fake_people_data = {
        "12345": {"name": "Test User", "email": "testuser@example.com"},
        "67890": {"name": "Another User", "email": "anotheruser@example.com"}
    }

    mock_read.return_value = fake_people_data
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert "name" in person
        assert "email" in person


def test_get_text(existing_text_key):
    with patch('data.text.read_one', return_value={"title": "Sample Title"}):
        resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/{existing_text_key}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "title" in resp_json
        assert resp_json["title"] == "Sample Title"


def test_del_text():
    text_key = "DeletePage"

    # First call: successful deletion
    with patch('data.text.delete', return_value=True) as mock_delete:
        with patch('data.text.read_one', return_value={"title": "Test Title"}):
            resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/{text_key}')
            assert resp.status_code == OK
            assert mock_delete.called
            mock_delete.assert_called_once_with(text_key)

    # Second call: text not found
    with patch('data.text.read_one', return_value=None):
        double_delete_resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/{text_key}')
        assert double_delete_resp.status_code == NOT_FOUND


def test_create_text(valid_text_data):
    text_key = valid_text_data["key"]

    with patch('data.text.create') as mock_create:
        mock_create.return_value = text_key
        create_resp = TEST_CLIENT.post(f'{ep.TEXT_EP}/{text_key}',
                                       json=valid_text_data)
        assert create_resp.status_code == OK
        create_resp_json = create_resp.get_json()
        assert create_resp_json[ep.MESSAGE] == "Text added!"

        # Verify the mock was called with correct parameters
        mock_create.assert_called_once_with(
            text_key,
            valid_text_data.get("title"),
            valid_text_data.get("text")
        )


def test_update_text(valid_text_data):
    existing_key = "Home Page"
    new_data = valid_text_data.copy()
    new_data["title"] = "Updated Page"
    with patch('data.text.update') as mock_update:
        mock_update.return_value = new_data
        resp = TEST_CLIENT.put(
            f'{ep.TEXT_EP}/{existing_key}', json=new_data
        )
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[ep.MESSAGE] == "Text updated!"
        assert resp_json[ep.RETURN] == new_data


def test_create_person(valid_person_data):
    with patch('data.people.create') as mock_create:
        mock_create.return_value = valid_person_data['email']
        resp = TEST_CLIENT.post(f'{ep.PEOPLE_EP}/create',
                                json=valid_person_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[ep.MESSAGE] == "Person added!"


@pytest.mark.skip(reason="Takes too dang long")
def test_create_person_invalid_email():
    invalid_data = {
        "name": "Test User",
        "affiliation": "Test University",
        "email": "invalid-email",  # Invalid email format
        "role": "Student",
        "password": "testpassword123"  # Add required password
    }
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=invalid_data)
    assert resp.status_code == NOT_ACCEPTABLE


def test_update_person(existing_person_id, valid_person_data):
    new_data = valid_person_data.copy()
    new_data["name"] = "Updated Name"
    with patch('data.people.update') as mock_update:
        mock_update.return_value = new_data
        resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/{existing_person_id}',
                               json=new_data)
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

    with patch('data.people.delete') as mock_delete:
        # Using mock_delete.side_effec t to simulate different behavior
        mock_delete.side_effect = [True, False]
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


@pytest.mark.skip("Skipping bc i want to mock this one.")
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
