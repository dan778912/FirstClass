# masthead.py

from data.people import has_role, read, NAME, EMAIL, AFFILIATION
import data.roles as rls

MH_FIELDS = [NAME, AFFILIATION]


def create_mh_rec(person: dict) -> dict:
    """
    Creates a simplified record for masthead use.
    """
    return {NAME: person[NAME], EMAIL: person[EMAIL]}


def get_masthead() -> dict:
    """
    Groups people by their roles for masthead use.
    Returns:
        dict: Dictionary where keys are role descriptions
              and values are lists of people with that role.
    """
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


def get_mh_fields(journal_code=None) -> list:
    """
    fetches masthead fields.
    - takes journal code in optionally
    - returns masthead fields in form of list
    """
    return MH_FIELDS


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
