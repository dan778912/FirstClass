"""
Tests for the manuscript module.
"""

import pytest
from unittest.mock import patch

import data.manuscripts as manuscripts
import data.manus.query as query


@patch('data.manuscripts.read')
def test_sort_manuscripts_by_state(mock_read):
    """
    Test that manuscripts are sorted correctly by state.
    """
    # Create mock manuscripts with different states
    mock_manuscripts = [
        {'manu_id': '1', 'curr_state': query.PUBLISHED},
        {'manu_id': '2', 'curr_state': query.SUBMITTED},
        {'manu_id': '3', 'curr_state': query.COPY_EDIT},
        {'manu_id': '4', 'curr_state': query.REJECTED},
        {'manu_id': '5', 'curr_state': 'INVALID_STATE'},  # Invalid state
    ]

    # Set up the mock to return our test data
    mock_read.return_value = mock_manuscripts

    # Call the function
    result = manuscripts.sort_manuscripts_by_state()

    # The expected order based on the actual VALID_STATES list
    # Create a dictionary of state indices for valid states
    state_indices = {}
    for state in query.VALID_STATES:
        state_indices[state] = query.VALID_STATES.index(state)

    # Sort manuscripts with valid states by their index in VALID_STATES
    valid_manuscripts = [m for m in mock_manuscripts
                         if m['curr_state'] in query.VALID_STATES]
    expected_manuscripts = sorted(
        valid_manuscripts,
        key=lambda m: state_indices[m['curr_state']]
    )

    # Add manuscripts with invalid states at the end
    invalid_manuscripts = [m for m in mock_manuscripts
                           if m['curr_state'] not in query.VALID_STATES]
    expected_manuscripts.extend(invalid_manuscripts)

    # Extract just the IDs for comparison
    expected_order = [m['manu_id'] for m in expected_manuscripts]

    # Check that the manuscripts are in the expected order
    actual_order = [m['manu_id'] for m in result]
    assert actual_order == expected_order, (
        f"Expected {expected_order}, got {actual_order}"
    )


@patch('data.manuscripts.read')
def test_filter_manuscripts_by_state(mock_read):
    """
    Test that manuscripts are filtered correctly by state.
    """
    # Create mock manuscripts with different states
    mock_manuscripts = [
        {'manu_id': '1', 'curr_state': query.PUBLISHED},
        {'manu_id': '2', 'curr_state': query.SUBMITTED},
        {'manu_id': '3', 'curr_state': query.SUBMITTED},
        {'manu_id': '4', 'curr_state': query.REJECTED},
    ]

    # Set up the mock to return our test data
    mock_read.return_value = mock_manuscripts

    # Call the function to filter for SUBMITTED manuscripts
    result = manuscripts.filter_manuscripts_by_state(query.SUBMITTED)

    # Should only return manuscripts with SUBMITTED state
    assert len(result) == 2
    assert all(m['curr_state'] == query.SUBMITTED for m in result)
    assert set(m['manu_id'] for m in result) == {'2', '3'}


def test_filter_manuscripts_by_invalid_state():
    """
    Test that an invalid state raises a ValueError.
    """
    with pytest.raises(ValueError):
        manuscripts.filter_manuscripts_by_state('INVALID_STATE')


if __name__ == '__main__':
    pytest.main(['-xvs', __file__])
