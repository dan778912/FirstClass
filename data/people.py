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
    print(f'{EMAIL=}, {email=}')
    return dbc.delete(PEOPLE_COLLECT, {EMAIL: email})


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


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_with_roles = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_with_roles.append(rec)
            masthead[text] = people_with_roles
        return masthead


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
