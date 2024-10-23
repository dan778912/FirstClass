# people.py

import data.roles as rls

NAME = "name"
ROLES = "roles"
AFFILIATION = "affiliation"
EMAIL = "email"

TEST_EMAIL = "aim9061@nyu.edu"
PROF_TEST_EMAIL = "ejc369@nyu.edu"


TEST_PERSON_DICT = {
    TEST_EMAIL: {
        NAME: "Alex Martin",
        ROLES: [],
        AFFILIATION: "NYU",
        EMAIL: TEST_EMAIL,
    },
    PROF_TEST_EMAIL: {
        NAME: "Eugene Callahan",
        ROLES: [],
        AFFILIATION: "NYU",
        EMAIL: PROF_TEST_EMAIL,
    },
}


def create(name: str, affiliation: str, email: str):
    """
    Creates a new entity Person.
    Returns new Person with fields: name, affiliation, email.
    Args:
        string: name, affiliation, email
    Returns:
        string: email value in dictionary
    """
    if email in TEST_PERSON_DICT:
        raise ValueError(f"Trying to add duplicate: {email=}")
    TEST_PERSON_DICT[email] = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email,
    }
    return TEST_PERSON_DICT[email]


def update(email: str, name=None, affiliation=None, new_email=None):
    """
    Updates a Person's name, affiliation, or email.

    Args:
        email (str): Current email of the person.
        name (str, optional): New name to update.
        affiliation (str, optional): New affiliation to update.
        new_email (str, optional): New email to update.

    Returns:
        dict: Updated person dictionary, or False if email not found.
    """
    if email not in TEST_PERSON_DICT:
        return False

    person = TEST_PERSON_DICT[email]

    if name:
        person[NAME] = name
    if affiliation:
        person[AFFILIATION] = affiliation
    if new_email and new_email != email:
        person[EMAIL] = new_email
        TEST_PERSON_DICT[new_email] = person
        del TEST_PERSON_DICT[email]

    return person


def read(email: str):
    """
    Reads information from Person fields and returns it.
    Args:
        string: email
    Returns:
        string: email value
    """
    return TEST_PERSON_DICT.get(email)


def delete(email: str):
    """
    Deletes given entity Person.
    Returns true if successfully deleted, and false if an error occurred.
    Args:
        string: email
    Returns:
        Bool: true if deleted, false if not.
    """
    if email in TEST_PERSON_DICT:
        del TEST_PERSON_DICT[email]
        return True
    return False


def get():
    """
    Takes in no arguments but returns a dictionary of users in which
    each user email must be the key for another dictionary.
    Args:
        None
    Returns:
        Dict: dictionary of users on user email
    """
    return TEST_PERSON_DICT
