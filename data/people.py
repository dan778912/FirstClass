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
    if email in TEST_PERSON_DICT:
        raise ValueError(f'Trying to add duplicate: {email=}')
    TEST_PERSON_DICT[email] = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email
    }
    return TEST_PERSON_DICT[email]


def update_person(email: str, name=None, affiliation=None):
    if email not in TEST_PERSON_DICT:
        return False
    if name:
        TEST_PERSON_DICT[email][NAME] = name
    if affiliation:
        TEST_PERSON_DICT[email][AFFILIATION] = affiliation
    return TEST_PERSON_DICT[email]


def read_person(email: str):
    return TEST_PERSON_DICT.get(email)


def delete_person(email: str):
    if email in TEST_PERSON_DICT:
        del TEST_PERSON_DICT[email]
        return True
    return False


def get_people():
    return TEST_PERSON_DICT
