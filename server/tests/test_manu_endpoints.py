import os
import sys
import pytest
from unittest.mock import patch
from http.client import NOT_FOUND, OK

# Add the parent directory to the path so we can import the modules
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import endpoints as ep  # noqa: E402

# Constants for endpoints
MANU_EP = '/manuscripts'
MESSAGE = 'Message'
RETURN = 'Return'

TEST_CLIENT = ep.app.test_client()


@pytest.fixture
def valid_manuscript_data():
    return {
        "title": "Test Manuscript",
        "author": "testuser@nyu.edu"
    }


@pytest.fixture
def existing_manuscript_id():
    return "manu123"


def test_get_manuscripts():
    fake_manuscripts = {
        "manu123": {
            "title": "Test Manuscript",
            "author": "testuser@nyu.edu",
            "curr_state": "SUBMITTED"
        },
        "manu456": {
            "title": "Another Manuscript",
            "author": "anotheruser@nyu.edu",
            "curr_state": "UNDER_REVIEW"
        }
    }

    with patch('data.manuscripts.read', return_value=fake_manuscripts):
        resp = TEST_CLIENT.get(MANU_EP)

        # Handle redirect if needed
        if resp.status_code == 308:
            resp = TEST_CLIENT.get(resp.location)

        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert isinstance(resp_json, dict)
        for manu_id, manuscript in resp_json.items():
            assert isinstance(manuscript, dict)
            assert "title" in manuscript
            assert "author" in manuscript
            assert "curr_state" in manuscript


def test_get_manuscripts_by_author():
    author = "testuser@nyu.edu"
    author_manuscripts = {
        "manu123": {
            "title": "Test Manuscript",
            "author": author,
            "curr_state": "SUBMITTED"
        }
    }

    with patch('data.manuscripts.get_manuscript',
               return_value=author_manuscripts):
        resp = TEST_CLIENT.get(f'{MANU_EP}/{author}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert isinstance(resp_json, dict)
        for manu_id, manuscript in resp_json.items():
            assert manuscript["author"] == author


def test_create_manuscript(valid_manuscript_data):
    manu_id = "new_manu_id"

    # Mock all the necessary functions
    with patch('data.manuscripts.create_manuscript',
               return_value=manu_id) as mock_create, \
         patch('data.people.exists', return_value=False) as mock_exists:
        resp = TEST_CLIENT.put(f'{MANU_EP}/create', json=valid_manuscript_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Manuscript created successfully!"
        assert resp_json[RETURN] == manu_id

        # Verify that create_manuscript was called with the right arguments
        mock_create.assert_called_once_with(
            valid_manuscript_data['title'],
            valid_manuscript_data['author']
        )

        # Verify that exists was called with the author email
        mock_exists.assert_called_once_with(valid_manuscript_data['author'])

    # Test with an existing author who doesn't have the AU role
    mock_person = {
        "name": "Test User",
        "email": valid_manuscript_data['author'],
        "roles": ["ED"],  # Has editor role but not author
        "affiliation": "Test University"
    }

    with patch('data.manuscripts.create_manuscript',
               return_value=manu_id), \
         patch('data.people.exists', return_value=True), \
         patch('data.people.read_one', return_value=mock_person), \
         patch('data.people.update',
               return_value=valid_manuscript_data['author']) as mock_update:
        resp = TEST_CLIENT.put(f'{MANU_EP}/create', json=valid_manuscript_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Manuscript created successfully!"
        assert resp_json[RETURN] == manu_id

        # Verify that update was called to add the AU role
        mock_update.assert_called_once_with(
            valid_manuscript_data['author'],
            mock_person["name"],
            mock_person["affiliation"],
            valid_manuscript_data['author'],
            ["ED", "AU"]  # Should have added AU to the roles
        )


def test_delete_manuscript(existing_manuscript_id):
    with patch('data.manuscripts.delete_manuscript', return_value=1):
        resp = TEST_CLIENT.delete(f'{MANU_EP}/delete/{existing_manuscript_id}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "Deleted" in resp_json

    # Test not found case
    with patch('data.manuscripts.delete_manuscript', return_value=0):
        resp = TEST_CLIENT.delete(f'{MANU_EP}/delete/nonexistent_id')
        assert resp.status_code == NOT_FOUND


def test_receive_action():
    manu_id = "manu123"
    action_data = {
        "manu_id": manu_id,
        "curr_state": "SUBMITTED",
        "action": "SEND_TO_REVIEW"
    }

    with patch('data.manuscripts.handle_action',
               return_value={"new_state": "UNDER_REVIEW"}):
        resp = TEST_CLIENT.put(f'{MANU_EP}/receive_action', json=action_data)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Action received!"
        assert "new_state" in resp_json[RETURN]


def test_state_transitions():
    fake_transitions = {
        "SUBMITTED": ["SEND_TO_REVIEW", "REJECT"],
        "UNDER_REVIEW": ["ACCEPT", "REJECT", "REVISE"]
    }

    with patch('data.manus.query.VALID_STATES', list(fake_transitions.keys())):
        with patch('data.manus.query.get_valid_actions_by_state',
                   side_effect=lambda state: fake_transitions.get(state, [])):
            resp = TEST_CLIENT.get(f'{MANU_EP}/state_transitions')
            assert resp.status_code == OK
            resp_json = resp.get_json()
            assert isinstance(resp_json, dict)
            for state, actions in resp_json.items():
                assert state in fake_transitions
                assert actions == fake_transitions[state]
