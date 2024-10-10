"""
This module interfaces to a data layer that endpoints make use of.
"""


def create_people():
    """
    Creates a new entity Person.
    Returns new Person with fields: name, affiliation, email.
    Args:
        string: name, affiliation, email_address
    Returns:
        Person: the new Person created.
    """
    pass


def update_people():
    """
    Updates given entity Person:
    Returns given entity with updated fields.
    Args:
        Person: person to be updated
        String: field to be updated
    Returns:
        Person: person that was updated
        Bool(?): maybe return a bool if person was not found or not updated?
    """
    pass


def read_people():
    """
    (btw this was the one i was least sure about, so pls edit if it's wrong)
    Reads information from Person fields and returns it
    Args:
        Person: entity you're reading information from
        String: field you want to read
    Returns:
        String: information from field you want to read
    """
    pass


def delete_people():
    """
    Deletes given entity Person.
    Returns true if successfully deleted, and false if an error occurred.

    Args:
        Person: entity to be deleted
    Returns:
        Bool: true if deleted, false if not.
    """
    pass


def get_people():
    """
    Takes in no arguments but returns a dictionary of users in which
    each user email must be the key for another dictionary.

    Args:
        None
    Returns:
        Dict: dictionary of users on user email
    """
