TITLE = 'title'
DISPLAY_NAME = 'display_name'

TEST_FIELD_NAME = TITLE
TEST_FIELD_DISPLAY_NAME = 'Title'


FIELDS = {
    TITLE: {
        DISPLAY_NAME: TEST_FIELD_DISPLAY_NAME
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