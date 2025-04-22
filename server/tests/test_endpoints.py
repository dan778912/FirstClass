import os
import sys
from unittest.mock import patch
from http.client import OK

# Add the parent directory to the path so we can import the modules
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import endpoints as ep  # noqa: E402

# Constants for endpoints
HELLO_EP = '/hello'
TITLE_EP = '/title'
ROLES_EP = '/roles'
ENDPOINT_EP = '/endpoints'
TITLE_RESP = 'Title'
HELLO_RESP = 'hello'
ENDPOINT_RESP = 'Available endpoints'

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(HELLO_EP)
    resp_json = resp.get_json()
    assert HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(TITLE_EP)
    resp_json = resp.get_json()
    assert TITLE_RESP in resp_json
    assert isinstance(resp_json[TITLE_RESP], str)


def test_endpoints():
    resp = TEST_CLIENT.get(ENDPOINT_EP)
    resp_json = resp.get_json()
    assert ENDPOINT_RESP in resp_json
    assert isinstance(resp_json[ENDPOINT_RESP], list)


def test_roles():
    with patch('data.roles.get_roles',
               return_value={"AU": "Author", "ED": "Editor"}):
        resp = TEST_CLIENT.get(ROLES_EP)
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert isinstance(resp_json, dict)
        assert "AU" in resp_json
        assert resp_json["AU"] == "Author"


def test_dev_info():
    """Test the /dev/info endpoint"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = b"test output"
        resp = TEST_CLIENT.get('/dev/info')
        assert resp.status_code == OK
        resp_json = resp.get_json()
        assert isinstance(resp_json, dict)
        assert "python_version" in resp_json
