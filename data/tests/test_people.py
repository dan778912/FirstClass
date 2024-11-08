# test_people.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import data.people as ppl
import pytest
from unittest.mock import patch
from data.roles import TEST_CODE


ADD_EMAIL = "callahan@nyu.edu"
TEMP_EMAIL = "temp_email@temp.com"

# Fixtures
@pytest.fixture(scope="function")
def temp_person():
    ret = ppl.create("John Doe", "NYU", TEMP_EMAIL, TEST_CODE)
    yield ret
    ppl.delete(ret)


@pytest.fixture(scope="function")
def duplicate_person():
    email = "duplicate@nyu.edu"
    ppl.create("Duplicate User", "NYU", email, TEST_CODE)
    yield email
    ppl.delete(email)


def test_get_people():
    """
    This is a test to ensure the function `get_people()` is running correctly.
    Checks to ensure people is a dict type, not empty, _id is str type, and
    NAME is in the dict.
    """
    people = ppl.get()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_create_person():
    """
    This is a test to ensure the function `create_person()` is correct.
    Checks to ensure ADD_EMAIL is in people after it is added (and not before).
    """
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, TEST_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_update_person():
    """
    This is a test to ensure the function `update_person()` is working.
    Checks to see if the name was updated after calling `update_person()`.
    """
    ppl.create("Update Test", "NYU", "updatetest@nyu.edu", TEST_CODE)
    updated_person = ppl.update("updatetest@nyu.edu",
                                name="Updated Name",
                                new_email="newemail@nyu.edu")

    people = ppl.get()

    assert updated_person["name"] == "Updated Name"

    assert "updatetest@nyu.edu" not in people
    assert "newemail@nyu.edu" in people
    assert updated_person["email"] == "newemail@nyu.edu"


def test_delete_person():
    """
    This is a test to ensure the function `delete_person()` is working.
    Checks to see if person is removed after deleting it.
    """
    people = ppl.read()
    old_len = len(people)
    ppl.delete(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


@pytest.fixture(scope='function')
def temp_person():
    ret = ppl.create("John Doe", "NYU", TEMP_EMAIL, TEST_CODE)
    yield ret
    ppl.delete(ret)


def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    assert ppl.read_one("Not an existing email!") is None


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create(
            "Irrelevant name",
            "Irrelevant affiliation",
            "invalid email",
            TEST_CODE
        )

# Check for duplicate email
def test_create_duplicate_person():
    duplicate_person = "duplicate@nyu.edu"
    ppl.create("Original User", "NYU", duplicate_person, TEST_CODE)
    with pytest.raises(ValueError, match="Trying to add duplicate: email="):
        ppl.create("Duplicate User", "NYU", duplicate_person, TEST_CODE)



@pytest.mark.skip(reason="Feature not yet implemented")
def test_partial_update_person():
    pass


@patch("data.people.read")
def test_get_people_mocked_read(mock_read):
    mock_read.return_value = {
        "mock_id": {ppl.NAME: "Mock User", ppl.AFFILIATION: "NYU"}
    }
    people = ppl.read()
    assert "mock_id" in people
    assert people["mock_id"][ppl.NAME] == "Mock User"


def test_create_person_with_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        ppl.create("Invalid Email User", "NYU", "invalid-email", TEST_CODE)


NO_AT = 'zcd220'
NO_NAME = '@nyu'
NO_DOMAIN = 'zcd220@'
NO_DOMAIN_EXTENSION = 'zcd220@nyu'
DOMAIN_TOO_SHORT = "zcd220@nyu.e"
DOMAIN_TOO_LONG = "zcd220@nyu.eduuuuu"
COMPLEX_EMAIL = 'zcd.220!220@n.y-u.edu'


def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_no_domain_extension():
    assert not ppl.is_valid_email(NO_DOMAIN_EXTENSION)


def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)


def test_is_valid_complex_email():
    assert ppl.is_valid_email(COMPLEX_EMAIL)
