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
WITHDRAW = 'WIT'   # Withdraw

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

def get_states() -> list:
    """
    Returns the list of valid manuscript states.
    
    Returns:
        list: All valid manuscript states
    """
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    """
    Checks if a given state is valid.
    
    Args:
        state (str): State to validate
        
    Returns:
        bool: True if state is valid, False otherwise
    """
    return state in VALID_STATES


def get_actions() -> list:
    """
    Returns the list of valid actions.
    
    Returns:
        list: All valid actions
    """
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    """
    Checks if a given action is valid.
    
    Args:
        action (str): Action to validate
        
    Returns:
        bool: True if action is valid, False otherwise
    """
    return action in VALID_ACTIONS


def assign_ref(manuscript: dict, ref: str, extra=None) -> str:
    """
    Handles the state transition when assigning a referee.
    
    Args:
        manuscript (dict): Manuscript data
        ref (str): New referee assigned to the manuscript
        
    Returns:
        str: New state after referee assignment (In Referee Review)
    """
    print(extra)
    manuscript[flds.REFEREES].append(ref)
    return IN_REF_REV


# State transition function identifier
FUNC = 'f'

# State transition table defining valid actions and their resulting states
STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: lambda m: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    IN_REF_REV: {},
    COPY_EDIT: {
        DONE: {
            FUNC: lambda m: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {},
    REJECTED: {},
    WITHDRAWN: {},
}


def get_valid_actions_by_state(state: str) -> set:
    """
    Gets all valid actions for a given state.
    
    Args:
        state (str): Current manuscript state
        
    Returns:
        set: Valid actions for the given state
    """
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state: str, action: str, manuscript: dict) -> str:
    """
    Processes a state transition based on the current state and action.
    
    Args:
        curr_state (str): Current manuscript state
        action (str): Action to perform
        manuscript (dict): Manuscript data
        
    Returns:
        str: New state after action is performed
        
    Raises:
        ValueError: If state or action is invalid
    """
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def main():
    """Test the state transition functionality."""
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANUSCRIPT))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANUSCRIPT))


if __name__ == '__main__':
    main()
