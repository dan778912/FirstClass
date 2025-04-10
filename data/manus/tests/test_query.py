import random
import pytest
import data.manus.query as mqry
import data.manus.fields as flds


def gen_random_not_valid_str() -> str:
    """Generates a random string that won't match any valid state or action."""
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    return str(big_int)


# State Tests
def test_is_valid_state():
    """Test that all defined states are recognized as valid."""
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    """Test that random strings are not recognized as valid states."""
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())


def test_states_are_unique():
    """Test that there are no duplicate states."""
    states = mqry.get_states()
    assert len(states) == len(set(states))


# Action Tests
def test_is_valid_action():
    """Test that all defined actions are recognized as valid."""
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_not_valid_action():
    """Test that random strings are not recognized as valid actions."""
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


def test_actions_are_unique():
    """Test that there are no duplicate actions."""
    actions = mqry.get_actions()
    assert len(actions) == len(set(actions))


# State Table Tests
def test_state_table_completeness():
    """Test that all states are present in the state table."""
    for state in mqry.get_states():
        assert state in mqry.STATE_TABLE


def test_state_table_actions_validity():
    """Test that all actions in state table are valid actions."""
    for state, actions in mqry.STATE_TABLE.items():
        for action in actions:
            assert mqry.is_valid_action(action)


# Transition Tests
def test_handle_action_bad_state():
    """Test that invalid states raise ValueError."""
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           mqry.SAMPLE_MANUSCRIPT)


def test_handle_action_bad_action():
    """Test that invalid actions raise ValueError."""
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           mqry.SAMPLE_MANUSCRIPT)


def test_handle_action_valid_return():
    """Test that all valid state-action combinations return valid states."""
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            if action in [mqry.DELETE_REF, mqry.ASSIGN_REF]:
                new_state = mqry.handle_action(
                    state, action, mqry.SAMPLE_MANUSCRIPT, ref="test@nyu.edu")
            else:
                new_state = mqry.handle_action(
                    state, action, mqry.SAMPLE_MANUSCRIPT)
            assert mqry.is_valid_state(new_state)


def test_specific_state_transitions():
    """Test specific known state transitions."""
    new_state = mqry.handle_action(
        mqry.SUBMITTED, mqry.ASSIGN_REF,
        mqry.SAMPLE_MANUSCRIPT, ref='test@nyu.edu')
    assert new_state == mqry.IN_REF_REV

    new_state = mqry.handle_action(
        mqry.SUBMITTED, mqry.REJECT, mqry.SAMPLE_MANUSCRIPT)
    assert new_state == mqry.REJECTED


def test_valid_actions_by_state():
    """Test that get_valid_actions_by_state returns correct actions."""
    # Check valid actions for the 'SUBMITTED' state
    submitted_actions = mqry.get_valid_actions_by_state(mqry.SUBMITTED)
    assert mqry.ASSIGN_REF in submitted_actions
    assert mqry.REJECT in submitted_actions
    assert mqry.WITHDRAW in submitted_actions

    # Check valid actions for the 'REJECTED' state
    rejected_actions = mqry.get_valid_actions_by_state(mqry.REJECTED)
    assert mqry.WITHDRAW in rejected_actions
    assert len(rejected_actions) == 1  # Only WITHDRAW should be valid.


def test_manuscript_immutability():
    """Test that state transitions don't modify the manuscript."""
    original_manu = mqry.SAMPLE_MANUSCRIPT.copy()
    mqry.handle_action(
        mqry.SUBMITTED, mqry.ASSIGN_REF,
        mqry.SAMPLE_MANUSCRIPT, ref='test@nyu.edu')
    assert mqry.SAMPLE_MANUSCRIPT == original_manu


@pytest.fixture
def sample_manuscript():
    """Fixture providing a test manuscript."""
    return {
        flds.TITLE: 'Test Title',
        flds.AUTHOR: 'Test Author',
        flds.REFEREES: ['Referee1', 'Referee2']
    }


def test_transitions_with_different_manuscripts(sample_manuscript):
    """Test that transitions work with different manuscript data."""
    new_state = mqry.handle_action(
        mqry.SUBMITTED, mqry.ASSIGN_REF,
        sample_manuscript, ref='test@nyu.edu')
    assert new_state == mqry.IN_REF_REV
