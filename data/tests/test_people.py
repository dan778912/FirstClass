# test_people.py
import sys
import os
from unittest.mock import MagicMock, patch
import pytest
import data.people as ppl
from data.roles import TEST_CODE
import data.db_connect as db
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../../')))

sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../../')))

ADD_EMAIL = "callahan@nyu.edu"
TEMP_EMAIL = "temp_email@temp.com"
TEST_DOC = {"name": "Professor Callahan", "affiliation": "NYU",
            "email": "callahan@nyu.edu", "roles": ["AU"]}


@pytest.fixture(scope="function")
def temp_person():
    email = "temp_email@temp.com"
    with patch("data.people.create") as mock_create:
        mock_create.return_value = email
        ppl.create("John Doe", "NYU", email, TEST_CODE)
        yield email
        with patch("data.people.delete") as mock_delete:
            mock_delete.return_value = True
            ppl.delete(email)


@pytest.fixture(scope="function")
def duplicate_person():
    email = "duplicate@nyu.edu"
    ppl.create("Duplicate User", "NYU", email, TEST_CODE)
    yield email
    ppl.delete(email)


@patch("data.people.dbc.client", new_callable=MagicMock)
def test_create_person(mock_client):
    db.client = mock_client
    mock_collection = mock_client["gamesDB"]["people"]

    mock_collection.find.return_value = []

    assert not ppl.exists(ADD_EMAIL)

    mock_collection.insert_one.return_value.inserted_id = "123"
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, TEST_CODE)

    mock_collection.insert_one.assert_called_once_with({
        "name": "Professor Callahan",
        "affiliation": "NYU",
        "email": ADD_EMAIL,
        "roles": [TEST_CODE],
    })

    mock_collection.find.return_value = [{"_id": "123", "email": ADD_EMAIL}]
    assert ppl.exists(ADD_EMAIL)


def test_update_person():
    mock_name = "Updated Name"
    mock_affiliation = "Columbia"
    mock_email = "updatetest@nyu.edu"
    mock_roles = [TEST_CODE]

    with patch('data.people.exists', return_value=True):
        with patch('data.people.is_valid_person', return_value=True):
            result = ppl.update(mock_name, mock_affiliation, mock_email,
                                mock_roles)

            assert result == mock_email


def test_delete_person():
    ppl.delete(TEMP_EMAIL)
    print("here")
    assert not ppl.exists(TEMP_EMAIL)


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
    duplicate_email = "duplicate@nyu.edu"
    with patch("data.people.exists", side_effect=[False, True]):
        ppl.create("Original User", "NYU", duplicate_email, TEST_CODE)
        with pytest.raises(ValueError, match=f"Trying to add duplicate: email='{duplicate_email}'"):
            ppl.create("Duplicate User", "NYU", duplicate_email, TEST_CODE)
    ppl.delete(duplicate_email)


@pytest.mark.skip(reason="Feature not yet implemented")
def test_partial_update_person():
    pass


def test_exists(temp_person):
    with patch("data.people.read_one", return_value={"email": temp_person}):
        assert ppl.exists(temp_person)  # Should return True


def test_doesnt_exist():
    non_existing_email = "nonexistent@nyu.edu / Email does not exist"
    with patch("data.people.read_one", return_value=None):
        assert not ppl.exists(non_existing_email)


@patch("data.people.read")
def test_get_people_mocked_read(mock_read):
    mock_read.return_value = {
        "mock_id": {"name": "Mock User", "affiliation": "NYU"}
    }
    people = ppl.read()
    assert "mock_id" in people
    assert people["mock_id"]["name"] == "Mock User"


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


@pytest.mark.parametrize("email",
                         [NO_AT, NO_NAME, NO_DOMAIN, NO_DOMAIN_EXTENSION,
                          DOMAIN_TOO_SHORT, DOMAIN_TOO_LONG])
def test_is_invalid_email(email):
    assert not ppl.is_valid_email(email)


def test_is_valid_complex_email():
    complex_email = "zcd.220!220@n.y-u.edu"
    assert ppl.is_valid_email(complex_email)
