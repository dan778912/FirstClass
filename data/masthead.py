# masthead.py

from data.people import has_role, read, NAME, EMAIL
import data.roles as rls


def create_mh_rec(person: dict) -> dict:  # Can be removed if not needed
    """
    Creates a simplified record for masthead use.
    """
    return {NAME: person[NAME], EMAIL: person[EMAIL]}


def get_masthead() -> dict:  # Can be removed if not needed
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


def update_masthead_person() -> bool:
    pass
