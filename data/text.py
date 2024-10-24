"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionPage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
}


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def create():
    """
    Creates text:
        - Text to add (str)
        - returns a dictionary of keys
    """
    pass


def delete():
    """
    Deletes text:
        - Text to delete (str)
        - returns True if deleted successfully, False otherwise
    """
    pass


def update():
    """
    Updates text:
        - text to update (str)
        - returns dictionary key that's updated
    """
    pass


def read_one(key: str) -> dict:
    """
    Retrieves the page dictionary for the given key.
    Args:
        key: The key used to look up the page dictionary.
    Returns:
        dict: The page dictionary corresponding to the key.
              If the key is not found, returns an empty dictionary.
    """
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def main():
    print(read())


if __name__ == '__main__':
    main()
