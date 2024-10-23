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
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


def test_del_person():
    """
    tests to ensure that successful status codes are received if
    person is successfully deleted. otherwise should return a 404 status code
    """
    person_id = "aim9061@nyu.edu"
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{person_id}')
    assert resp.status_code == 200

    double_delete_resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{person_id}')
    assert double_delete_resp.status_code == 404
