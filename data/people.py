# people.py
import re

import data.roles as rls
from data.roles import PERSON_ROLES

NAME = "name"
ROLES = "roles"
ROLE = "role"
AFFILIATION = "affiliation"
EMAIL = "email"

TEST_EMAIL = "aim9061@nyu.edu"
PROF_TEST_EMAIL = "ejc369@nyu.edu"
DEL_EMAIL = 'delete@nyu.edu'


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
    DEL_EMAIL: {
        NAME: 'Another Person',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    }
}


LOCAL_CHARS = r'[A-Za-z0-9.!#$%&\'*+-/=?^_`{|}~]+'
DOMAIN_CHARS = r'[A-Za-z0-9.-]+'
DOMAIN_EXTENSION_CHARS = r'[A-Za-z]{2,3}'


def is_valid_email(email: str) -> bool:
    return re.match(
        f"^{LOCAL_CHARS}@{DOMAIN_CHARS}\\.{DOMAIN_EXTENSION_CHARS}$",
        email
    )


def is_valid_person(
    name: str,
    affiliation: str,
    email: str,
    role: str = None,
    roles: list = None
) -> bool:
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            print("these are person roles: ", PERSON_ROLES)
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def has_role(person: dict, role: str) -> bool:
    """
    Checks if a person has a specified role.
    Args:
        person (dict): The person's data dictionary.
        role (str): The role to check for.
    Returns:
        bool: True if the role is found in the person's roles, False otherwise.
    """
    return role in person.get(ROLES, [])


def create(name: str, affiliation: str, email: str, role: str):
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
    if is_valid_person(name, affiliation, email, role=role):
        roles = []
        if role:
            roles.append(role)
        TEST_PERSON_DICT[email] = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: roles
        }
        return email


def update(email: str, name=None, affiliation=None, new_email=None, role=None):
    """
    Updates a Person's name, affiliation, or email.

    Args:
        email (str): Current email of the person.
        name (str, optional): New name to update.
        affiliation (str, optional): New affiliation to update.
        new_email (str, optional): New email to update.
        role (str, optional): New role to add to roles list.

    Returns:
        dict: Updated person dictionary, or False if email not found.
    """
    if email not in TEST_PERSON_DICT:
        raise ValueError(
            f'Trying to update person that does not exist: '
            f'{email=}'
        )

    person = TEST_PERSON_DICT[email]

    if name:
        person[NAME] = name
    if affiliation:
        person[AFFILIATION] = affiliation
    if role:
        if ROLES not in person:
            person[ROLES] = []
        if role not in person[ROLES]:
            person[ROLES].append(role)
    if new_email and new_email != email:
        if new_email in TEST_PERSON_DICT:
            raise ValueError('Email already in use')
        person[EMAIL] = new_email
        TEST_PERSON_DICT[new_email] = person
        del TEST_PERSON_DICT[email]

    return person


def read():
    """
    Reads information from Person fields and returns it.
    Args:
        string: email
    Returns:
        string: email value
    """
    people = TEST_PERSON_DICT
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
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


def get(role=None, affiliation=None):
    """
    Takes in no arguments but returns a dictionary of users in which
    each user email must be the key for another dictionary.
    Args:
        None
    Returns:
        Dict: dictionary of users on user email
    """
    if not role and not affiliation:
        return TEST_PERSON_DICT

    filtered_dict = {}
    for email, person in TEST_PERSON_DICT.items():
        if role and role in person.get(ROLES, []):
            filtered_dict[email] = person
        elif affiliation and person.get(AFFILIATION) == affiliation:
            filtered_dict[email] = person

    return filtered_dict
