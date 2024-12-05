TITLE = 'title'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
STATE = 'state'
REFEREES = 'referees'
REPORT = 'report'
VERDICT = 'verdict'
TEXT = 'text'
ABSTRACT = 'abstract'
HISTORY = 'history'
EDITOR = 'editor'

# Attribute Keys
DISPLAY_NAME = 'display_name'

# Test Field Names
TEST_FIELD_TITLE_DISPLAY_NAME = 'Title'
TEST_FIELD_AUTHOR_DISPLAY_NAME = 'Author'
TEST_FIELD_AUTHOR_EMAIL_DISPLAY_NAME = 'Author Email'
TEST_FIELD_STATE_DISPLAY_NAME = 'State'
TEST_FIELD_REFEREES_DISPLAY_NAME = 'Referees'
TEST_FIELD_TEXT_DISPLAY_NAME = 'Text'
TEST_FIELD_ABSTRACT_DISPLAY_NAME = 'Abstract'
TEST_FIELD_HISTORY_DISPLAY_NAME = 'History'
TEST_FIELD_EDITOR_DISPLAY_NAME = 'Editor'

FIELDS = {
    TITLE: {DISPLAY_NAME: TEST_FIELD_TITLE_DISPLAY_NAME},
    AUTHOR: {DISPLAY_NAME: TEST_FIELD_AUTHOR_DISPLAY_NAME},
    AUTHOR_EMAIL: {DISPLAY_NAME: TEST_FIELD_AUTHOR_EMAIL_DISPLAY_NAME},
    STATE: {DISPLAY_NAME: TEST_FIELD_STATE_DISPLAY_NAME},
    REFEREES: {DISPLAY_NAME: TEST_FIELD_REFEREES_DISPLAY_NAME},
    TEXT: {DISPLAY_NAME: TEST_FIELD_TEXT_DISPLAY_NAME},
    ABSTRACT: {DISPLAY_NAME: TEST_FIELD_ABSTRACT_DISPLAY_NAME},
    HISTORY: {DISPLAY_NAME: TEST_FIELD_HISTORY_DISPLAY_NAME},
    EDITOR: {DISPLAY_NAME: TEST_FIELD_EDITOR_DISPLAY_NAME},
}


def get_fields() -> dict:
    """
    Return the dictionary of fields and their attributes.
    """
    return FIELDS


def get_field_names() -> list:
    """
    Return a list of field names.
    """
    return list(FIELDS.keys())


def get_display_name(field_name: str) -> str:
    """
    Return the display name for a given field name.
    If the field name does not exist, return an empty string.
    """
    field = FIELDS.get(field_name, {})
    return field.get(DISPLAY_NAME, '')


def is_field_valid(field_name: str) -> bool:
    """
    Check if a field name exists in the FIELDS dictionary.
    """
    return field_name in FIELDS


def add_field(field_name: str, display_name: str) -> bool:
    """
    Add a new field with its display name to the FIELDS dictionary.
    If the field name already exists, return False.
    """
    if field_name in FIELDS:
        return False  # Field already exists
    FIELDS[field_name] = {DISPLAY_NAME: display_name}
    return True


def update_field_display_name(field_name: str, new_display_name: str) -> bool:
    """
    Update the display name of an existing field.
    If the field name does not exist, return False.
    """
    if field_name not in FIELDS:
        return False  # Field does not exist
    FIELDS[field_name][DISPLAY_NAME] = new_display_name
    return True


def remove_field(field_name: str) -> bool:
    """
    Remove a field from the FIELDS dictionary.
    If the field name does not exist, return False.
    """
    if field_name not in FIELDS:
        return False  # Field does not exist
    del FIELDS[field_name]
    return True


# Functions derived from professor's code
def get_flds() -> dict:
    """
    Return the FIELDS dictionary.
    Added for compatibility with the professor's code.
    """
    return FIELDS


def get_fld_names() -> list:
    """
    Return field names as a list.
    Added for compatibility with the professor's code.
    """
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> str:
    """
    Return the display name for a given field name.
    Added for compatibility with the professor's code.
    """
    fld = FIELDS.get(fld_nm, {})
    return fld.get(DISPLAY_NAME, '')


def main():
    """
    Main function for testing.
    """
    print(f'Fields: {get_fields()}')
    print(f'Field Names: {get_field_names()}')
    print(f'Title Display Name: {get_display_name(TITLE)}')
    print(f'Is "title" valid? {is_field_valid(TITLE)}')

    # Test adding a new field
    print(f'Adding new field: {add_field("new_field", "New Field")}')
    print(f'Fields after adding: {get_fields()}')

    # Test updating a field display name
    print(f'Updating "title" display name: {update_field_display_name(TITLE, "Updated Title")}')
    print(f'Fields after updating: {get_fields()}')

    # Test removing a field
    print(f'Removing "new_field": {remove_field("new_field")}')
    print(f'Fields after removing: {get_fields()}')

    # Test professor's functions
    print(f'Fields (Professor): {get_flds()}')
    print(f'Field Names (Professor): {get_fld_names()}')
    print(f'Display Name for Title (Professor): {get_disp_name(TITLE)}')


if __name__ == '__main__':
    main()
