import random
import pytest
import data.manuscripts.query as mqry
import data.manuscripts.fields as flds

def gen_random_not_valid_str() -> str:
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    return str(big_int)

def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)

def test_is_not_valid_state():
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())

def test_states_are_unique():
    states = mqry.get_states()
    assert len(states) == len(set(states))

def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)

def test_is_not_valid_action():
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())

def test_actions_are_unique():
    actions = mqry.get_actions()
    assert len(actions) == len(set(actions))

def test_state_table_completeness():
    for state in mqry.get_states():
        assert state in mqry.STATE_TABLE

def test_state_table_actions_validity():
    for state, actions in mqry.STATE_TABLE.items():
        for action in actions:
            assert mqry.is_valid_action(action)

def test_handle_action_valid_return():
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            new_state = mqry.handle_action(state, action, mqry.SAMPLE_MANUSCRIPT, ref="Test Ref")
            assert mqry.is_valid_state(new_state)

def test_specific_state_transitions():
    new_state = mqry.handle_action(mqry.SUBMITTED, mqry.ASSIGN_REF, mqry.SAMPLE_MANUSCRIPT, ref="Assigned Referee")
    assert new_state == mqry.IN_REF_REV

    new_state = mqry.handle_action(mqry.SUBMITTED, mqry.REJECT, mqry.SAMPLE_MANUSCRIPT)
    assert new_state == mqry.REJECTED

def test_valid_actions_by_state():
    submitted_actions = mqry.get_valid_actions_by_state(mqry.SUBMITTED)
    assert mqry.ASSIGN_REF in submitted_actions
    assert mqry.REJECT in submitted_actions

    rejected_actions = mqry.get_valid_actions_by_state(mqry.REJECTED)
    assert len(rejected_actions) == 0

def test_manuscript_immutability():
    original_manu = mqry.SAMPLE_MANUSCRIPT.copy()
    mqry.handle_action(mqry.SUBMITTED, mqry.ASSIGN_REF, mqry.SAMPLE_MANUSCRIPT, ref="Test Ref")
    assert mqry.SAMPLE_MANUSCRIPT == original_manu

@pytest.fixture
def sample_manuscript():
    return {
        flds.TITLE: 'Test Title',
        flds.AUTHOR: 'Test Author',
        flds.REFEREES: ['Referee1', 'Referee2']
    }

def test_transitions_with_different_manuscripts(sample_manuscript):
    new_state = mqry.handle_action(mqry.SUBMITTED, mqry.ASSIGN_REF, sample_manuscript, ref="New Ref")
    assert new_state == mqry.IN_REF_REV
