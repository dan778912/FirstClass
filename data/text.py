import data.db_connect as dbc
"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'
TEXT_COLLECT = "text"


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = dbc.read_dict(TEXT_COLLECT, KEY)
    print(f'{text=}')
    return text


def create(key: str, title: str, text: str) -> bool:
    """
    Creates text:
        - takes key, title, text (all str)
        - returns True if created successfully, False otherwise
    """
    # check if dict exists
    existing = read_one(key)
    if existing:
        return key
    txt = {
        KEY: key,
        TITLE: title,
        TEXT: text
    }
    if dbc.create(TEXT_COLLECT, txt):
        return key
    else:
        return None


def delete(key: str) -> bool:
    """
    Deletes text:
        - Text to delete (str)
        - returns True if deleted successfully, False otherwise
    """
    if not read_one(key):
        return False
    print(f'{KEY=}, {key=}')
    return dbc.delete(TEXT_COLLECT, {KEY: key})


def update(key: str, title: str = None, text: str = None) -> bool:
    """
    Updates text:
        -   key to update (str),
            title to update (optional),
            text to update (optional)
        -   returns True if updated successfully, False otherwise
    """
    if read_one(key) is None:
        raise ValueError(
            f'Trying to update person that does not exist: '
            f'{key=}'
        )
    update_data = {
        KEY: key,
        TITLE: title,
        TEXT: text
    }
    ret = dbc.update(TEXT_COLLECT,
                     {KEY: key},
                     update_data)
    print(f'Update result: {ret=}')
    return key


def read_one(key: str) -> dict:
    """
    Retrieves the page dictionary for the given key.
    Args:
        key: The key used to look up the page dictionary.
    Returns:
        dict: The page dictionary corresponding to the key.
              If the key is not found, returns an empty dictionary.
    """
    return dbc.read_one(TEXT_COLLECT, {KEY: key})
