# people.py
import re

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
    Returns the email used as the key.
    Args:
        string: name, affiliation, email, role
    Returns:
        string: email value in dictionary
    """
    if exists(email):
        raise ValueError(f"Trying to add duplicate: {email=}")
    if is_valid_person(name, affiliation, email, role=role):
        roles = []
        if role:
            roles.append(role)
        person = {NAME: name, AFFILIATION: affiliation,
                  EMAIL: email, ROLES: roles}
        print(person)
        dbc.create(PEOPLE_COLLECT, person)
        return email


def update(name: str, affiliation: str, email: str, roles: list):
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
    if not exists(email):
        raise ValueError(
            f'Trying to update person that does not exist: '
            f'{email=}'
        )
    if is_valid_person(name, affiliation, email, roles=roles):
        ret = dbc.update(PEOPLE_COLLECT,
                         {EMAIL: email},
                         {NAME: name, AFFILIATION: affiliation,
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
