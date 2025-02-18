import data.db_connect as dbc


ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = '_id'
# REFEREE = 'referee'
REFEREES = 'referees'
TITLE = 'title'

TEST_ID = 'fake_id'
TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'

FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}

# states:
AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'
TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
]


def create_manuscript(title: str, author: str) -> str:
    """
    Creates a new manuscript in the database.
    Args:
        title: str - Title of the manuscript
        author: str - Author of the manuscript
    Returns:
        str: ID of the created manuscript
    """
    manuscript = {
        TITLE: title,
        AUTHOR: author,
        REFEREES: [],
        CURR_STATE: SUBMITTED  # All new manuscripts start in SUBMITTED state
    }
    manu_id = dbc.create('manuscripts', manuscript)
    return manu_id


def get_manuscript(manu_id: str) -> dict:
    """
    Retrieves a manuscript from the database.
    Args:
        manu_id: str - ID of the manuscript to retrieve
    Returns:
        dict: The manuscript document, or None if not found
    """
    return dbc.read_one('manuscripts', {MANU_ID: manu_id})


def update_manuscript(manu_id: str, updates: dict) -> bool:
    """
    Updates a manuscript in the database.
    Args:
        manu_id: str - ID of the manuscript to update
        updates: dict - Dictionary of fields to update
    Returns:
        bool: True if update was successful
    """
    return dbc.update('manuscripts', {MANU_ID: manu_id}, updates)


# actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'
# for testing:
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW,
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    manu[REFEREES].append(referee)
    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[REFEREES]) > 0:
        manu[REFEREES].remove(referee)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


FUNC = 'f'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REV,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REV: {
        **COMMON_ACTIONS,
    },
    REJECTED: {
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(manu_id, curr_state, action, **kwargs) -> str:
    """
    Handle an action on a manuscript.
    """
    # Get the manuscript from the database instead of using SAMPLE_MANU
    manus = get_manuscript(manu_id)
    if not manus:
        raise ValueError(f'Manuscript not found: {manu_id}')

    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')

    # Execute the action and get the new state
    new_state = STATE_TABLE[curr_state][action][FUNC](**kwargs, manu=manus)

    # Update the manuscript in the database with the new state
    update_manuscript(manu_id, {CURR_STATE: new_state})

    return new_state


def main():
    print(handle_action(TEST_ID, SUBMITTED, ASSIGN_REF, ref='Jack'))
    print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
                        ref='Jill', extra='Extra!'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jill'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jack'))
    print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))
    print(handle_action(TEST_ID, SUBMITTED, REJECT))


if __name__ == '__main__':
    main()
