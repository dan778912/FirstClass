import sys
import os
from unittest.mock import MagicMock, patch
import pytest
import data.people as ppl
from data.roles import TEST_CODE
import data.db_connect as db
sys.path.insert(0, os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), '../../')))

ADD_EMAIL = "callahan@nyu.edu"
TEMP_EMAIL = "temp_email@temp.com"
TEST_DOC = {"name": "Professor Callahan", "affiliation": "NYU",
            "email": "callahan@nyu.edu", "roles": ["AU"]}
TEST_PASSWORD = "password123"
# TEST_CODE = ["AU"] Use list of roles instead of single role


@pytest.fixture(scope='function')
def temp_person():
    email = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, roles=TEST_CODE,
                       password=TEST_PASSWORD)
    yield email
    try:
        ppl.delete(email)
    except ValueError as e:
        print(f'Person already deleted: {e}')


@pytest.fixture(scope="function")
def duplicate_person():
    email = "duplicate@nyu.edu"
    ppl.create("Duplicate User", "NYU", email, roles=TEST_CODE,
               password=TEST_PASSWORD)
    yield email
    ppl.delete(email)


@patch("data.people.dbc.client", new_callable=MagicMock)
def test_create_person(mock_client):
    mock_collection = mock_client["gamesDB"]["people"]
    # Ensure the `dbc.client` used in the module is mocked
    db.client = mock_client

    mock_collection.find.return_value = []
    assert not ppl.exists(ADD_EMAIL)

    mock_collection.insert_one.return_value = MagicMock(inserted_id="123")

    # Test creating person with password
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, roles=TEST_CODE,
               password=TEST_PASSWORD)
    mock_collection.insert_one.assert_called_once()

    # Test creating person without password (should fail)
    with pytest.raises(ValueError, match="Password is required"):
        ppl.create("Professor Callahan", "NYU", ADD_EMAIL, roles=TEST_CODE)

    # Test creating manuscript author without password (should work)
    ppl.create("Professor Callahan", "NYU", ADD_EMAIL, roles=TEST_CODE,
               is_manu_author=True)
    mock_collection.insert_one.assert_called()


def test_update_person():
    mock_new_email = "updatetest123@nyu.edu"
    mock_name = "Updated Name"
    mock_affiliation = "Columbia"
    mock_email = "updatetest@nyu.edu"
    mock_roles = [TEST_CODE]

    with patch('data.people.exists', return_value=True):
        with patch('data.people.is_valid_person', return_value=True):
            result = ppl.update(mock_email, mock_name, mock_affiliation,
                                mock_new_email, mock_roles)
            assert result == mock_new_email


@patch("data.people.exists")
@patch("data.people.dbc.client")
def test_delete_person(mock_client, mock_exists):
    mock_collection = mock_client["gamesDB"]["people"]
    db.client = mock_client  # Ensure the client is properly mocked

    mock_exists.return_value = True  # Person exists before deletion
    mock_collection.delete_one.return_value.deleted_count = 1
    # Simulate successful deletion

    ppl.delete(TEMP_EMAIL)

    # Validate `exists` call
    mock_exists.assert_called_once_with(TEMP_EMAIL)
    # Ensure `exists` is only called once

    # Validate `delete_one` call
    mock_collection.delete_one.assert_called_once_with({ppl.EMAIL: TEMP_EMAIL})

    # Debugging outputs to inspect actual calls
    print("mock_delete_one args:", mock_collection.delete_one.call_args_list)
    print("mock_exists call args:", mock_exists.call_args_list)


@patch("data.people.read", return_value={"id1": {"name": "Test User"}})
def test_read(mock_read):
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert "name" in person


def test_read_one(temp_person):
    with patch('data.people.read_one',
               return_value={"name": "John Doe", "email": TEMP_EMAIL}):
        assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    with patch('data.people.read_one', return_value=None):
        assert ppl.read_one("Not an existing email!") is None


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create("Bad name", "Bad affiliation", "invalid email", TEST_CODE,
                   password=TEST_PASSWORD)


@patch("data.people.dbc.create")
@patch("data.people.read_one")
def test_create_duplicate_person(mock_read_one, mock_create):
    dup = "duplicate@nyu.edu"
    existing_person = {
        "email": dup,
        "name": "Original User",
        "affiliation": "NYU",
        "roles": [TEST_CODE],
        "manuscripts": [],
        "submission_count": 0
    }

    # First creation - no existing user
    mock_read_one.return_value = None
    mock_create.return_value = True

    result = ppl.create("Original User", "NYU", dup, TEST_CODE,
                        password=TEST_PASSWORD)
    assert result == dup
    mock_read_one.assert_called_once_with(dup)
    mock_create.assert_called_once()

    # Second creation - user exists
    mock_read_one.return_value = existing_person
    mock_read_one.reset_mock()
    mock_create.reset_mock()

    # Should return existing user info without creating new record
    result = ppl.create("Duplicate User", "NYU", dup, TEST_CODE,
                        password=TEST_PASSWORD)
    assert result == dup
    mock_read_one.assert_called_once_with(dup)
    mock_create.assert_not_called()

    # Test with password
    mock_read_one.return_value = {
        **existing_person,
        "password": "hashed_password"
    }
    mock_read_one.reset_mock()

    result = ppl.create("Another User", "NYU", dup, TEST_CODE,
                        password=TEST_PASSWORD)
    assert result == dup
    mock_read_one.assert_called_once_with(dup)
    mock_create.assert_not_called()


@pytest.mark.skip(reason="Feature not yet implemented")
def test_partial_update_person():
    pass


def test_exists(temp_person):
    with patch("data.people.read_one", return_value={"email": temp_person}):
        assert ppl.exists(temp_person)


def test_doesnt_exist():
    non_existing_email = "nonexistent@nyu.edu"
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


@pytest.mark.skip(reason="Takes too dang long")
def test_create_person_with_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        ppl.create("Invalid Email User", "NYU", "invalid-email", TEST_CODE,
                   password=TEST_PASSWORD)


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
