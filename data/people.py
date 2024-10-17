# people.py

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
        raise ValueError(f'Trying to add duplicate: {email=}')
    TEST_PERSON_DICT[email] = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email
    }
    return TEST_PERSON_DICT[email]


def update(email: str, name=None, affiliation=None):
    """
    Updates given entity Person:
    Returns given entity with updated fields.
    Args:
        email (str): Email to update
        name (str, optional): Name to update. Defaults to None.
        affiliation (str, optional): Affiliation to update. Defaults to None.
    Returns:
        Bool: False (if email not in test_person_dict)
        string: email value otherwise
    """
    if email not in TEST_PERSON_DICT:
        return False
    if name:
        TEST_PERSON_DICT[email][NAME] = name
    if affiliation:
        TEST_PERSON_DICT[email][AFFILIATION] = affiliation
    return TEST_PERSON_DICT[email]


def read(email: str):
    """
    Reads information from Person fields and returns it
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
