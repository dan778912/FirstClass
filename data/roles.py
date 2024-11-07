# roles.py

"""
This module manages person roles for a journal.
"""
AUTHOR_CODE = 'AU'
ED_CODE = 'ED'
ME_CODE = 'ME'
CE_CODE = 'CE'
RE_CODE = 'RE'
CONSULT_CODE = 'CO'
TS_CODE = 'TS'
TEST_CODE = AUTHOR_CODE

PERSON_ROLES = {
    AUTHOR_CODE: 'Author',
    CONSULT_CODE: 'Consulting Editor',
    CE_CODE: 'Copy Editor',
    ED_CODE: 'Editor',
    ME_CODE: 'Managing Editor',
    RE_CODE: 'Referee',
    TS_CODE: 'Typesetter'

}

MASTHEAD_ROLES = [CE_CODE, ED_CODE, ME_CODE]


def get_roles() -> dict:
    return PERSON_ROLES


def get_role_codes() -> list:
    return list(PERSON_ROLES.keys())


def get_masthead_roles() -> dict:
    return {code: name for code, name in PERSON_ROLES.items() if code in
            MASTHEAD_ROLES}


def is_valid(code: str) -> bool:
    return code in PERSON_ROLES


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == '__main__':
    main()
