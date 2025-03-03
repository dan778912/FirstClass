import data.db_connect as dbc
import data.manus.query as query
import random
from mnemonic import Mnemonic

ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = 'manu_id'
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
        if not dbc.read_one('manuscripts', {MANU_ID: key}):
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
        REFEREES: {},
        CURR_STATE: SUBMITTED  # All new manuscripts start in SUBMITTED state
    }
    manu_id = dbc.create('manuscripts', manuscript)
    if manu_id is None:
        raise ValueError("Failed to create manuscript")
    else:
        return id


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
    result = dbc.update('manuscripts', {MANU_ID: manu_id}, updates)
    print(dbc.read_one('manuscripts', {MANU_ID: manu_id}))
    return result

# Commenting out because we just pull directly from query file
# # actions:
# ACCEPT = 'ACC'
# ASSIGN_REF = 'ARF'
# DELETE_REF = 'DRF'
# DONE = 'DON'
# REJECT = 'REJ'
# WITHDRAW = 'WIT'
# AUTHOR
# # for testing:
# TEST_ACTION = ACCEPT

# VALID_ACTIONS = [
#     ACCEPT,
#     ASSIGN_REF,
#     DELETE_REF,
#     DONE,
#     REJECT,
#     WITHDRAW,
# ]


def get_actions() -> list:
    return query.VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in query.VALID_ACTIONS


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

# COMMON_ACTIONS = {
#     WITHDRAW: {
#         FUNC: lambda **kwargs: WITHDRAWN,
#     },
# }

# STATE_TABLE = {
#     SUBMITTED: {
#         ASSIGN_REF: {
#             FUNC: lambda manuscript, ref='Default Ref', **kwargs:
#                 assign_ref(manuscript, ref),
#         },
#         REJECT: {
#             FUNC: lambda manuscript, **kwargs: REJECTED,
#         },
#         WITHDRAW: {
#             FUNC: lambda manuscript, **kwargs: WITHDRAWN,
#         },
#     },
#     IN_REF_REV: {
#         ACCEPT: {
#             FUNC: lambda manuscript, **kwargs: COPY_EDIT,
#         },
#         ASSIGN_REF: {
#             FUNC: lambda manuscript, ref='Default Ref', **kwargs:
#                 assign_ref(manuscript, ref),
#         },
#         DELETE_REF: {
#             FUNC: lambda manuscript, ref='Default Ref', **kwargs:
#                 delete_ref(manuscript, ref),
#         },
#         REJECT: {
#             FUNC: lambda manuscript, **kwargs: REJECTED,
#         },
#         WITHDRAW: {
#             FUNC: lambda manuscript, **kwargs: WITHDRAWN,
#         },
#     },
#     COPY_EDIT: {
#         DONE: {
#             FUNC: lambda manuscript, **kwargs: query.AUTHOR_REVIEW,
#         },
#     },
#     query.AUTHOR_REVIEW: {
#         DONE: {
#             FUNC: lambda manuscript, **kwargs: query.FORMATTING,
#         },
#         WITHDRAW: {
#             FUNC: lambda manuscript, **kwargs: WITHDRAWN,
#         },
#     },
#     query.FORMATTING: {
#         DONE: {
#             FUNC: lambda manuscript, **kwargs: query.PUBLISHED,
#         },
#     },
#     query.EDITOR_REVIEW: {
#         ACCEPT: {
#             FUNC: lambda manuscript, **kwargs: COPY_EDIT,
#         },
#         REJECT: {
#             FUNC: lambda manuscript, **kwargs: REJECTED,
#         },
#     },
#     REJECTED: {
#         WITHDRAW: {
#             FUNC: lambda manuscript, **kwargs: WITHDRAWN,
#         },
#     },
#     query.PUBLISHED: {},
#     WITHDRAWN: {},
# }


def get_valid_actions_by_state(state: str):
    valid_actions = query.STATE_TABLE[state].keys()
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

    if curr_state not in query.STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in query.STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')

    # Execute the action and get the new state
    new_state = query.STATE_TABLE[curr_state][action][FUNC](
                                            **kwargs, manuscript=manus)
    # new_state = (
    #     query.STATE_TABLE[curr_state][action][FUNC](
    #         **kwargs, manu=manus
    #     )
    # )

    # Update the manuscript in the database with the new state
    update_manuscript(manu_id, {CURR_STATE: new_state})

    return new_state


def main():
    # print(handle_action(TEST_ID, SUBMITTED, ASSIGN_REF, ref='Jack'))
    # print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
    #                     ref='Jill', extra='Extra!'))
    # print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
    #                     ref='Jill'))
    # print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
    #                     ref='Jack'))
    # print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))
    # print(handle_action(TEST_ID, SUBMITTED, REJECT))
    print(generate_id())


if __name__ == '__main__':
    main()
