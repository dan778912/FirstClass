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

DISPLAY_NAME = 'Display Name'

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
    TITLE: {
        DISPLAY_NAME: TEST_FIELD_TITLE_DISPLAY_NAME
    },
    AUTHOR: {
        DISPLAY_NAME: TEST_FIELD_AUTHOR_DISPLAY_NAME
    },
    AUTHOR_EMAIL: {
        DISPLAY_NAME: TEST_FIELD_AUTHOR_EMAIL_DISPLAY_NAME
    },
    STATE: {
        DISPLAY_NAME: TEST_FIELD_STATE_DISPLAY_NAME
    },
    REFEREES: {
        DISPLAY_NAME: TEST_FIELD_REFEREES_DISPLAY_NAME
    },
    TEXT: {
        DISPLAY_NAME: TEST_FIELD_TEXT_DISPLAY_NAME
    },
    ABSTRACT: {
        DISPLAY_NAME: TEST_FIELD_ABSTRACT_DISPLAY_NAME
    },
    HISTORY: {
        DISPLAY_NAME: TEST_FIELD_HISTORY_DISPLAY_NAME
    },
    EDITOR: {
        DISPLAY_NAME: TEST_FIELD_EDITOR_DISPLAY_NAME
    }
}


def get_fields() -> dict:
    return FIELDS


def get_field_names() -> list:
    return FIELDS.keys()


def get_display_name(field_name: str) -> dict:
    field = FIELDS.get(field_name, '')
    display_name = field.get(DISPLAY_NAME, '')
    return display_name


def main():
    print(f'{get_fields()=}')


if __name__ == '__main__':
    main()