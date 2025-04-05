# fields.py

# Field Names
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
TEST_FIELD_REPORT_DISPLAY_NAME = 'Report'
TEST_FIELD_VERDICT_DISPLAY_NAME = 'Verdict'

# State Display Names
STATE_SUBMITTED_DISPLAY_NAME = 'Submitted'
STATE_IN_REF_REV_DISPLAY_NAME = 'In Referee Review'
STATE_EDITOR_REVIEW_DISPLAY_NAME = 'Editor Review'
STATE_COPY_EDIT_DISPLAY_NAME = 'Copy Editing'
STATE_AUTHOR_REVIEW_DISPLAY_NAME = 'Author Review'
STATE_FORMATTING_DISPLAY_NAME = 'Formatting'
STATE_PUBLISHED_DISPLAY_NAME = 'Published'
STATE_REJECTED_DISPLAY_NAME = 'Rejected'
STATE_WITHDRAWN_DISPLAY_NAME = 'Withdrawn'

FIELDS = {
    TITLE: {DISPLAY_NAME: TEST_FIELD_TITLE_DISPLAY_NAME},
    AUTHOR: {DISPLAY_NAME: TEST_FIELD_AUTHOR_DISPLAY_NAME},
    AUTHOR_EMAIL: {DISPLAY_NAME: TEST_FIELD_AUTHOR_EMAIL_DISPLAY_NAME},
    STATE: {DISPLAY_NAME: TEST_FIELD_STATE_DISPLAY_NAME},
    REFEREES: {DISPLAY_NAME: TEST_FIELD_REFEREES_DISPLAY_NAME},
    REPORT: {DISPLAY_NAME: TEST_FIELD_REPORT_DISPLAY_NAME},
    VERDICT: {DISPLAY_NAME: TEST_FIELD_VERDICT_DISPLAY_NAME},
    TEXT: {DISPLAY_NAME: TEST_FIELD_TEXT_DISPLAY_NAME},
    ABSTRACT: {DISPLAY_NAME: TEST_FIELD_ABSTRACT_DISPLAY_NAME},
    HISTORY: {DISPLAY_NAME: TEST_FIELD_HISTORY_DISPLAY_NAME},
    EDITOR: {DISPLAY_NAME: TEST_FIELD_EDITOR_DISPLAY_NAME},
}

# State mappings
STATE_DISPLAY_NAMES = {
    'SUB': STATE_SUBMITTED_DISPLAY_NAME,
    'REV': STATE_IN_REF_REV_DISPLAY_NAME,
    'EDR': STATE_EDITOR_REVIEW_DISPLAY_NAME,
    'CED': STATE_COPY_EDIT_DISPLAY_NAME,
    'AUR': STATE_AUTHOR_REVIEW_DISPLAY_NAME,
    'FMT': STATE_FORMATTING_DISPLAY_NAME,
    'PUB': STATE_PUBLISHED_DISPLAY_NAME,
    'REJ': STATE_REJECTED_DISPLAY_NAME,
    'WIT': STATE_WITHDRAWN_DISPLAY_NAME,
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


def get_state_display_name(state_code: str) -> str:
    """
    Return the display name for a given state code.
    If the state code does not exist, return an empty string.
    """
    return STATE_DISPLAY_NAMES.get(state_code, '')


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
