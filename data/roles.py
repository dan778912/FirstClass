# roles.py

"""
This module manages person roles for a journal.
"""
AUTHOR_CODE = 'AU'
ED_CODE = 'ED'
ME_CODE = 'ME'
CE_CODE = 'CE'
RE_CODE = 'RE'
TEST_CODE = AUTHOR_CODE

PERSON_ROLES = {
    AUTHOR_CODE: 'Author',
    CE_CODE: 'Consulting Editor',
    ED_CODE: 'EDITOR',
    ME_CODE: 'Managing Editor',
    RE_CODE: 'Referee',
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
