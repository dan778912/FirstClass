# test_people.py
import sys
import os
from unittest.mock import patch
import pytest
import data.people as ppl
from data.roles import TEST_CODE, ME_CODE
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
    assert not ppl.exists(ADD_EMAIL)
    # Create the person
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, TEST_CODE)
    assert ppl.exists(ADD_EMAIL)
    ppl.delete(ADD_EMAIL)


def test_update_person():
    mock_name = "Updated Name"
    mock_affiliation = "Columbia"
    mock_email = "updatetest@nyu.edu"
    mock_roles = [TEST_CODE]
    with patch('data.dbc.update',
               return_value={"name": mock_name, "email": mock_email}
               ) as mock_db_update:
        with patch('data.people.exists', return_value=True):
            with patch('data.people.is_valid_person', return_value=True):
                result = ppl.update(mock_name, mock_affiliation, mock_email,
                                    mock_roles)

                assert result == mock_email
                mock_db_update.assert_called_once_with(
                    "people_collection",
                    {EMAIL: mock_email},
                    {
                        NAME: mock_name,
                        AFFILIATION: mock_affiliation,
                        EMAIL: mock_email,
                        ROLES: mock_roles
                    }
                )


def test_delete_person():
    ppl.delete(TEMP_EMAIL)
    assert not ppl.exists(temp_person)


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


def test_exists(temp_person):
    assert ppl.exists(temp_person)


def test_doesnt_exist():
    assert not ppl.exists('Not an existing email!')


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
