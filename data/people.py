# people.py
import re
from werkzeug.security import generate_password_hash, check_password_hash

import data.roles as rls
from data.roles import PERSON_ROLES
import data.db_connect as dbc

client = dbc.connect_db()
print(f'{client=}')

PEOPLE_COLLECT = 'people'
MIN_USER_NAME_LEN = 2

NAME = "name"
ROLES = "roles"
ROLE = "role"
AFFILIATION = "affiliation"
EMAIL = "email"
PASSWORD = "password"
MANUSCRIPTS = "manuscripts"
SUBMISSION_COUNT = "submission_count"


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


def create(name: str, affiliation: str, email: str, role: str,
           password: str = None) -> str:
    """
    Creates a new entity Person.
    Returns the email used as the key.
    Args:
        string: name, affiliation, email, role
        password: optional password for authentication
    Returns:
        string: email value in dictionary
    """
    # Check if person already exists
    existing = read_one(email)
    if existing:
        return email

    if is_valid_person(name, affiliation, email, role=role):
        person = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: [role],
            MANUSCRIPTS: [],
            SUBMISSION_COUNT: 0
        }
        if password:
            person[PASSWORD] = generate_password_hash(password)

        if dbc.create(PEOPLE_COLLECT, person):
            return email
    return None


def update(curr_email: str, name: str, affil: str, email: str, roles: list):
    """
    Updates a Person's name, affiliation, roles, or email
    Args:
        name (str, optional): New name to update.
        affiliation (str, optional): New affiliation to update.
        email (str): Current email of the person.
        roles (list, optional): New roles to add to roles list.

    Returns:
        string: email value in dictionary
    """
    if not exists(curr_email):
        raise ValueError(
            f'Trying to update person that does not exist: '
            f'{curr_email=}'
        )
    if is_valid_person(name, affil, curr_email, roles=roles):
        ret = dbc.update(PEOPLE_COLLECT,
                         {EMAIL: curr_email},
                         {NAME: name, AFFILIATION: affil,
                          EMAIL: email, ROLES: roles})
        print(f'{ret=}')
        return email


def read() -> dict:
    """
    Reads information from Person fields and returns it.
    Args:
        None
    Returns:
        dict: dictionary of users keyed by email
    """
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    print(f'{people=}')
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
    """
    return dbc.read_one(PEOPLE_COLLECT, {EMAIL: email})


def exists(email: str) -> bool:
    return read_one(email) is not None


def delete(email: str):
    """
    Deletes given entity Person.
    Returns the person deleted.
    Args:
        string: email
    Returns:
        Bool: DB person entry.
    """
    if not exists(email):
        raise ValueError(f"Person does not exist: {email=}")
    print(f'{EMAIL=}, {email=}')
    return dbc.delete(PEOPLE_COLLECT, {EMAIL: email})


def authenticate(email: str, password: str) -> dict:
    """
    Authenticate a person with email and password
    Returns None if authentication fails
    """
    person = read_one(email)
    if not person or not person.get(PASSWORD):
        return None

    if check_password_hash(person[PASSWORD], password):
        return person
    return None


def add_manuscript(email: str, manuscript_id: str) -> bool:
    """
    Add a manuscript ID to person's list of submissions
    """
    person = read_one(email)
    if not person:
        return False

    manuscripts = person.get(MANUSCRIPTS, [])
    if manuscript_id not in manuscripts:
        manuscripts.append(manuscript_id)

    update = {
        MANUSCRIPTS: manuscripts,
        SUBMISSION_COUNT: len(manuscripts)
    }

    return dbc.update_one(PEOPLE_COLLECT, {EMAIL: email}, {"$set": update})


def get_manuscripts(email: str) -> list:
    """
    Get list of manuscript IDs submitted by person
    """
    person = read_one(email)
    if not person:
        return []
    return person.get(MANUSCRIPTS, [])
