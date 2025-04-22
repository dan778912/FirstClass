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
TEXT_EP = '/text'
MESSAGE = 'Message'
RETURN = 'Return'

TEST_CLIENT = ep.app.test_client()


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


def test_get_text(existing_text_key):
    test_data = {"title": "Sample Title", "text": "Test Text"}
    with patch('data.text.read_one', return_value=test_data):
        resp = TEST_CLIENT.get(f'{TEXT_EP}/{existing_text_key}')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert "title" in resp_json


def test_del_text():
    text_key = "DeletePage"

    # First call: successful deletion
    with patch('data.text.delete', return_value=True) as mock_delete:
        with patch('data.text.read_one', return_value={"title": "Test Title"}):
            resp = TEST_CLIENT.delete(f'{TEXT_EP}/{text_key}')
            assert resp.status_code == OK
            assert mock_delete.called
            mock_delete.assert_called_once_with(text_key)

    # Second call: text not found
    with patch('data.text.read_one', return_value=None):
        double_delete_resp = TEST_CLIENT.delete(f'{TEXT_EP}/{text_key}')
        assert double_delete_resp.status_code == NOT_FOUND


def test_create_text(valid_text_data):
    text_key = valid_text_data["key"]

    with patch('data.text.create') as mock_create:
        mock_create.return_value = text_key
        create_resp = TEST_CLIENT.post(f'{TEXT_EP}/{text_key}',
                                       json=valid_text_data)
        assert create_resp.status_code == OK
        create_resp_json = create_resp.get_json()
        assert create_resp_json[MESSAGE] == "Text added!"

        # Verify the mock was called with correct parameters
        mock_create.assert_called_once_with(
            valid_text_data["key"],
            valid_text_data["title"],
            valid_text_data["text"]
        )


def test_update_text(valid_text_data):
    existing_key = valid_text_data["key"]
    new_data = valid_text_data.copy()
    new_data["title"] = "Updated Title"

    with patch('data.text.update') as mock_update:
        mock_update.return_value = new_data
        resp = TEST_CLIENT.put(
            f'{TEXT_EP}/{existing_key}', json=new_data
        )
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert resp_json[MESSAGE] == "Text updated!"
        assert resp_json[RETURN] == new_data
