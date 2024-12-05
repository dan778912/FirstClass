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
        # Define any possible transitions here, if applicable
    },
}


def handle_action(curr_state, action, manuscript=None) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')

    # Check if the action is valid for the current state
    if curr_state not in STATE_TABLE or action not in STATE_TABLE[curr_state]:
        raise AssertionError(
            f"Invalid state transition: {curr_state} -> {action}"
        )

    # Perform the action and determine the new state
    transition = STATE_TABLE[curr_state][action]
    new_state = transition[FUNC](manuscript)
    
    # Validate the new state
    if not is_valid_state(new_state):
        raise AssertionError(
            f"Invalid state transition: {curr_state} -> {action} -> {new_state}"
        )

    return new_state
