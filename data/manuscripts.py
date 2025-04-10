import data.db_connect as dbc
import data.manus.query as query
import data.manus.fields as flds
import random
from mnemonic import Mnemonic

ACTION = 'action'
AUTHOR = flds.AUTHOR
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = 'manu_id'
TITLE = flds.TITLE
MANU_COLLECT = "manuscripts"

TEST_ID = 'fake_id'
TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'

FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}


def generate_id() -> str:
    """
    Generates a unique ID for a manuscript.
    Returns:
        str: The generated ID.
    NOTE: This function will loop endlessly if a collision occurs.
    """
    mnemo = Mnemonic('english')
    while True:
        # Generate 32 hex characters (128 bits of entropy)
        entropy = ''.join(random.choices('0123456789abcdef', k=32))
        words = mnemo.to_mnemonic(bytes.fromhex(entropy))
        key = "".join(words.split()[:3])
        # If the key doesn't exist in the database, return it
        if not dbc.read_one(MANU_COLLECT, {MANU_ID: key}):
            return key


def create_manuscript(title: str, author: str) -> str:
    """
    Creates a new manuscript in the database.
    Args:
        title: str - Title of the manuscript
        author: str - Author of the manuscript
    Returns:
        str: ID of the created manuscript
    """
    id = generate_id()
    manuscript = {
        MANU_ID: id,
        TITLE: title,
        AUTHOR: author,
        flds.REFEREES: [],  # Initialize as empty list for referee assignments
        CURR_STATE: query.SUBMITTED  # all start as submitted
    }
    manu_id = dbc.create(MANU_COLLECT, manuscript)
    if manu_id is None:
        raise ValueError("Failed to create manuscript")
    else:
        return id


def read_one(manu_id: str) -> dict:
    return dbc.read_one(MANU_COLLECT, {MANU_ID: manu_id})


def get_manuscript(author: str) -> dict:
    """
    Retrieves a manuscript from the database based on author.
    Args:
        manu_id: str - ID of the manuscript to retrieve
    Returns:
        dict: The manuscript document, or None if not found
    """
    author_manu = []
    manu_list = read()
    for manu in manu_list:
        if manu[AUTHOR] == author:
            author_manu.append(manu)
    return author_manu
    # return dbc.read_one(MANU_COLLECT, {MANU_ID: manu_id})


def read() -> dict:
    """
    Reads information from Person fields and returns it.
    Args:
        None
    Returns:
        dict: dictionary of users keyed by email
    """
    manu_list = []
    for manu in dbc.fetch_all(MANU_COLLECT):
        dbc.convert_mongo_id(manu)
        manu_list.append(manu)
    return manu_list


def update_manuscript(manu_id: str, updates: dict) -> bool:
    """
    Updates a manuscript in the database.
    Args:
        manu_id: str - ID of the manuscript to update
        updates: dict - Dictionary of fields to update
    Returns:
        bool: True if update was successful
    """
    result = dbc.update(MANU_COLLECT, {MANU_ID: manu_id}, updates)
    return result


def delete_manuscript(manu_id: str) -> bool:
    """
    Deletes a manuscript from the database.
    Args:
        manu_id: str - ID of the manuscript to delete
    Returns:
        bool: True if deletion was successful
    """
    result = dbc.delete(MANU_COLLECT, {MANU_ID: manu_id})
    return result


def get_actions() -> list:
    return query.VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in query.VALID_ACTIONS


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    manu[flds.REFEREES].append(referee)
    return query.IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(referee)
    if len(manu[flds.REFEREES]) > 0:
        return query.IN_REF_REV
    else:
        return query.SUBMITTED


FUNC = 'f'


def handle_action(manu_id, curr_state, action, **kwargs) -> str:
    """
    Handle an action on a manuscript.
    """
    # Get the manuscript from the database instead of using SAMPLE_MANU
    manus = read_one(manu_id)
    if not manus:
        raise ValueError(f'Manuscript not found: {manu_id}')

    if curr_state not in query.STATE_TABLE:
        raise ValueError(f'Action not available: {curr_state}')
    if action not in query.STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    # Execute the action and get the new state

    new_state = query.STATE_TABLE[curr_state][action][FUNC](
                                            manuscript=manus, **kwargs)
    # Update the manuscript in database with both state and any modified fields
    updates = {
        CURR_STATE: new_state,
        flds.REFEREES: manus[flds.REFEREES]  # Include the updated ref list
    }
    update_manuscript(manu_id, updates)
    return new_state
