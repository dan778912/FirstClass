# test_people.py
import sys
import os
from unittest.mock import patch
import pytest
import data.people as ppl
from data.roles import TEST_CODE
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../../')))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

ADD_EMAIL = "callahan@nyu.edu"
TEMP_EMAIL = "temp_email@temp.com"


@pytest.fixture(scope="function")
def temp_person():
    with patch('data.people.create') as mock_create:
        mock_create.return_value = TEMP_EMAIL
        _id = mock_create("John Doe", "NYU", TEMP_EMAIL, TEST_CODE)
        yield _id
        with patch('data.people.delete') as mock_delete:
            mock_delete(_id)


@pytest.fixture(scope="function")
def duplicate_person():
    email = "duplicate@nyu.edu"
    ppl.create("Duplicate User", "NYU", email, TEST_CODE)
    yield email
    ppl.delete(email)


def test_get_people():
    with patch("data.people.read", return_value={"mock_id": {ppl.NAME: "Mock User"}}):
        people = ppl.get()
        assert isinstance(people, dict)
        assert len(people) > 0
        for _id, person in people.items():
            assert isinstance(_id, str)
            assert ppl.NAME in person


def test_create_person():
    """
    This test ensures the `create_person` function works
    by adding an email to the people dictionary.
    """
    people = ppl.read()
    # Check that ADD_EMAIL is not already present
    assert ADD_EMAIL not in people

    # Create the person
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, TEST_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_update_person():
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
    with patch("data.people.delete") as mock_delete:
        ppl.delete(TEMP_EMAIL)
        mock_delete.assert_called_once_with(TEMP_EMAIL)


def test_read():
    with patch("data.people.read", return_value={"id1": {"name": "Test User"}}):
        people = ppl.read()
        assert isinstance(people, dict)
        assert len(people) > 0
        for _id, person in people.items():
            assert isinstance(_id, str)
            assert ppl.NAME in person


def test_read_one(temp_person):
    with patch('data.people.read_one', return_value={"name": "John Doe", "email": TEMP_EMAIL}):
        assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    with patch('data.people.read_one', return_value=None):
        assert ppl.read_one("Not an existing email!") is None


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create("Irrelevant name", "Irrelevant affiliation", "invalid email", TEST_CODE)


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


@pytest.mark.parametrize("email", [NO_AT, NO_NAME, NO_DOMAIN, NO_DOMAIN_EXTENSION, DOMAIN_TOO_SHORT, DOMAIN_TOO_LONG])
def test_is_invalid_email(email):
    assert not ppl.is_valid_email(email)


def test_is_valid_complex_email():
    assert ppl.is_valid_email(COMPLEX_EMAIL)
