import data.manuscripts.fields as fields

# States
AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
TEST_STATE = SUBMITTED

VALID_STATES = [
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    AUTHOR_REV,
]

SAMPLE_MANUSCRIPT = {
    fields.TITLE: 'Short module import names in Python',
    fields.AUTHOR: 'Zoe Dauphinee',
    fields.REFEREES: []
}


def get_states() -> list:
    """Return the list of valid states."""
    return VALID_STATES

def is_valid_state(state: str) -> bool:
    """Check if a state is valid."""
    return state in VALID_STATES

# Actions
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
]

def get_actions() -> list:
    """Return the list of valid actions."""
    return VALID_ACTIONS

def is_valid_action(action: str) -> bool:
    """Check if an action is valid."""
    return action in VALID_ACTIONS

def get_valid_actions_by_state(state: str) -> list:
    if state not in STATE_TABLE:
        return []
    return list(STATE_TABLE[state].keys())


# State Table and Transitions
FUNC = 'f'

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda m: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            FUNC: lambda m: COPY_EDIT,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    COPY_EDIT: {  # Ensure this transition exists
        DONE: {
            FUNC: lambda m: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {
        DONE: {
            FUNC: lambda m: SUBMITTED,
        },
    },
    REJECTED: {
        # Define possible next steps, like resubmission
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state, action, manuscript) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Invalid state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'Invalid action: {action}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def main():
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANUSCRIPT))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANUSCRIPT))


if __name__ == '__main__':
    main()
