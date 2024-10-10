"""
This module interfaces to a data layer that endpoints make use of.
"""

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
        EMAIL: TEST_EMAIL
    },
    PROF_TEST_EMAIL: {
        NAME: "Eugene Callahan",
        ROLES: [],
        AFFILIATION: "NYU",
        EMAIL: PROF_TEST_EMAIL
    },
}


def create_person(name: str, affiliation: str, email: str):
    """
    Creates a new entity Person.
    Returns new Person with fields: name, affiliation, email.
    Args:
        string: name, affiliation, email_address
    Returns:
        None
    """
    if email in TEST_PERSON_DICT:
        raise ValueError(f'Trying to add duplicate: {email=}')
    TEST_PERSON_DICT[email] = {NAME: name, AFFILIATION: affiliation, 
                               EMAIL: email}


def update_people():
    """
    Updates given entity Person:
    Returns given entity with updated fields.
    Args:
        Person: person to be updated
        String: field to be updated
    Returns:
        Person: person that was updated
        Bool(?): maybe return a bool if person was not found or not updated?
    """
    pass


def read_people():
    """
    (btw this was the one i was least sure about, so pls edit if it's wrong)
    Reads information from Person fields and returns it
    Args:
        Person: entity you're reading information from
        String: field you want to read
    Returns:
        String: information from field you want to read
    """
    pass


def delete_people(_id):
    """
    Deletes given entity Person.
    Returns true if successfully deleted, and false if an error occurred.

    Args:
        Person: person id to be deleted
    Returns:
        Bool: true if deleted, false if not.
    """
    pass


def get_people():
    """
    Takes in no arguments but returns a dictionary of users in which
    each user email must be the key for another dictionary.

    Args:
        None
    Returns:
        Dict: dictionary of users on user email
    """
    people = TEST_PERSON_DICT
    return people
