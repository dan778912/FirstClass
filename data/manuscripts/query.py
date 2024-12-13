"""
This module handles manuscript state management and transitions.
It defines valid states, actions, and the rules for transitioning between states.
"""
import data.manuscripts.fields as flds

# Manuscript States
AUTHOR_REV = 'AUR'  # Author Revision
COPY_EDIT = 'CED'   # Copy Editing
IN_REF_REV = 'REV'  # In Referee Review
REJECTED = 'REJ'    # Rejected
SUBMITTED = 'SUB'   # Submitted
WITHDRAWN = 'WIT'   # Withdrawn

TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN
]

# Manuscript Actions
ACCEPT = 'ACC'      # Accept
ASSIGN_REF = 'ARF'  # Assign Referee
DELETE_REF = 'DRF'  # Delete Referee
DONE = 'DON'        # Done
REJECT = 'REJ'      # Reject
WITHDRAW = 'WIT'    # Withdraw

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW
]

# Sample manuscript for testing
SAMPLE_MANUSCRIPT = {
    flds.TITLE: 'Short module import names in Python',
    flds.AUTHOR: 'Eugene Callahan',
    flds.REFEREES: [],
}

FUNC = 'f'

# Reusable transitions for common actions
COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda manuscript, **kwargs: WITHDRAWN,  # Accept positional arguments
    },
}

def get_states() -> list:
    return VALID_STATES

def is_valid_state(state: str) -> bool:
    return state in VALID_STATES

def get_actions() -> list:
    return VALID_ACTIONS

def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

def assign_ref(manuscript: dict, ref: str, extra=None) -> str:
    manuscript[flds.REFEREES].append(ref)
    return IN_REF_REV

def delete_ref(manuscript: dict, ref: str) -> str:
    if len(manuscript[flds.REFEREES]) > 0:
        manuscript[flds.REFEREES].remove(ref)
    if len(manuscript[flds.REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs: assign_ref(manuscript, ref),
        },
        REJECT: {
            FUNC: lambda manuscript, **kwargs: REJECTED,
        },
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs: assign_ref(manuscript, ref),
        },
        DELETE_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs: delete_ref(manuscript, ref),
        },
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda manuscript, **kwargs: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    REJECTED: {
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    WITHDRAWN: {
    },
}


def get_valid_actions_by_state(state: str) -> set:
    """
    Gets all valid actions for a given state.

    Args:
        state (str): Current manuscript state

    Returns:
        set: Valid actions for the given state
    """
    if state not in STATE_TABLE:
        return set()
    valid_actions = STATE_TABLE[state].keys()
    return set(valid_actions)


def handle_action(curr_state: str, action: str, manuscript: dict, **kwargs) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript, **kwargs)
