"""
This module handles manuscript state management and transitions.
It defines valid states, actions, and the rules for transitions.
"""

import data.manus.fields as flds


# Manuscript States
AUTHOR_REVIEW = 'AUR'  # Author Review
COPY_EDIT = 'CED'      # Copy Editing
EDITOR_REVIEW = 'EDR'  # Editor Review
FORMATTING = 'FMT'     # Formatting
IN_REF_REV = 'REV'    # In Referee Review
PUBLISHED = 'PUB'      # Published
REJECTED = 'REJ'       # Rejected
SUBMITTED = 'SUB'      # Submitted
WITHDRAWN = 'WIT'      # Withdrawn

TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REVIEW,
    COPY_EDIT,
    EDITOR_REVIEW,
    FORMATTING,
    IN_REF_REV,
    PUBLISHED,
    REJECTED,
    SUBMITTED,
    WITHDRAWN
]

# Manuscript Actions
ACCEPT = 'ACC'         # Accept
ASSIGN_REF = 'ARF'     # Assign Referee
DELETE_REF = 'DRF'     # Delete Referee
DONE = 'DON'          # Done
EDITOR_MOVE = 'EMV'    # Editor Move (can transition to any state)
REJECT = 'REJ'        # Reject
WITHDRAW = 'WIT'      # Withdraw

TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    EDITOR_MOVE,
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


def assign_ref(manuscript: dict, ref: str, extra=None) -> str:
    """
    Assign a referee to a manuscript.

    Args:
        manuscript: The manuscript dictionary
        ref: The referee to assign
        extra: Optional extra data

    Returns:
        str: The new state after assigning the referee
    """
    manuscript[flds.REFEREES].append(ref)
    return IN_REF_REV


def delete_ref(manuscript: dict, ref: str) -> str:
    """
    Delete a referee from a manuscript.

    Args:
        manuscript: The manuscript dictionary
        ref: The referee to delete

    Returns:
        str: The new state after deleting the referee
    """
    if len(manuscript[flds.REFEREES]) > 0:
        manuscript[flds.REFEREES].remove(ref)
    if len(manuscript[flds.REFEREES]) > 0:
        return IN_REF_REV
    return SUBMITTED


def editor_move(manu: dict, target_state: str = SUBMITTED, **kwargs) -> str:
    """
    Special function to allow editor to move to any valid state.

    Args:
        manuscript: The manuscript dictionary
        target_state: The target state to move to
        **kwargs: Additional keyword arguments

    Returns:
        str: The new target state if valid

    Raises:
        ValueError: If the target state is invalid
    """
    if target_state in VALID_STATES:
        return target_state
    raise ValueError(f'Invalid target state: {target_state}')


# State transition table
STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs:
                assign_ref(manuscript, ref),
        },
        REJECT: {
            FUNC: lambda manuscript, **kwargs: REJECTED,
        },
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            FUNC: lambda manuscript, **kwargs: COPY_EDIT,
        },
        ASSIGN_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs:
                assign_ref(manuscript, ref),
        },
        DELETE_REF: {
            FUNC: lambda manuscript, ref='Default Ref', **kwargs:
                delete_ref(manuscript, ref),
        },
        REJECT: {
            FUNC: lambda manuscript, **kwargs: REJECTED,
        },
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda manuscript, **kwargs: AUTHOR_REVIEW,
        },
    },
    AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda manuscript, **kwargs: FORMATTING,
        },
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda manuscript, **kwargs: PUBLISHED,
        },
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda manuscript, **kwargs: COPY_EDIT,
        },
        REJECT: {
            FUNC: lambda manuscript, **kwargs: REJECTED,
        },
    },
    REJECTED: {
        WITHDRAW: {
            FUNC: lambda manuscript, **kwargs: WITHDRAWN,
        },
    },
    PUBLISHED: {},
    WITHDRAWN: {},
}


def get_states() -> list:
    """Return the list of valid states."""
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    """Check if a state is valid."""
    return state in VALID_STATES


def get_actions() -> list:
    """Return the list of valid actions."""
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    """Check if an action is valid."""
    return action in VALID_ACTIONS


def get_valid_actions_by_state(state: str) -> set:
    """
    Gets all valid actions for a given state.

    Args:
        state: Current manuscript state

    Returns:
        set: Valid actions for the given state
    """
    if state not in STATE_TABLE:
        return set()
    valid_actions = STATE_TABLE[state].keys()
    return set(valid_actions)


def handle_action(curr_state: str, action: str, manu: dict, **kwargs) -> str:
    """
    Handle a state transition action.

    Args:
        curr_state: Current state
        action: Action to perform
        manu: Manuscript dictionary
        **kwargs: Additional keyword arguments

    Returns:
        str: The new state after the action

    Raises:
        ValueError: If the state or action is invalid
    """
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')

    # Handle editor move separately
    if action == EDITOR_MOVE:
        target_state = kwargs.get('target_state', SUBMITTED)
        return editor_move(manu, target_state)

    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manu, **kwargs)
