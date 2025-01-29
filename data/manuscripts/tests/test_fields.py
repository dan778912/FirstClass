import pytest
from data.manuscripts import fields as fld

def test_get_fields():
    """
    Test that get_fields returns a dictionary.
    """
    fields = fld.get_fields()
    assert isinstance(fields, dict), "get_fields should return a dictionary"
    assert len(fields) > 0, "Fields dictionary should not be empty"


def test_get_field_names():
    """
    Test that get_field_names returns a list of field names.
    """
    field_names = fld.get_field_names()
    assert isinstance(field_names, list), "get_field_names should return a list"
    assert all(isinstance(name, str) for name in field_names), "Field names should be strings"


def test_get_display_name():
    """
    Test that get_display_name returns the correct display name for a field.
    """
    assert fld.get_display_name(fld.TITLE) == "Title", "Display name for 'title' should be 'Title'"
    assert fld.get_display_name("nonexistent") == "", "Display name for an unknown field should be an empty string"


def test_is_field_valid():
    """
    Test that is_field_valid correctly identifies valid and invalid fields.
    """
    assert fld.is_field_valid(fld.TITLE), "'title' should be a valid field"
    assert not fld.is_field_valid("nonexistent"), "'nonexistent' should not be a valid field"


def test_add_field():
    """
    Test that add_field correctly adds a new field.
    """
    new_field = "new_field"
    display_name = "New Field"
    assert fld.add_field(new_field, display_name), "Should successfully add a new field"
    assert fld.is_field_valid(new_field), "The new field should now be valid"
    assert fld.get_display_name(new_field) == display_name, "The display name should match the new field"

    # Test adding a duplicate field
    assert not fld.add_field(new_field, display_name), "Should not allow adding a duplicate field"


def test_update_field_display_name():
    """
    Test that update_field_display_name correctly updates the display name.
    """
    updated_display_name = "Updated Title"
    assert fld.update_field_display_name(fld.TITLE, updated_display_name), "Should successfully update the display name"
    assert fld.get_display_name(fld.TITLE) == updated_display_name, "The display name should be updated"

    # Test updating a non-existent field
    assert not fld.update_field_display_name("nonexistent", "New Name"), "Should not update a non-existent field"


def test_remove_field():
    """
    Test that remove_field correctly removes a field.
    """
    new_field = "field_to_remove"
    display_name = "Field to Remove"
    fld.add_field(new_field, display_name)

    assert fld.is_field_valid(new_field), "Field should be valid before removal"
    assert fld.remove_field(new_field), "Should successfully remove the field"
    assert not fld.is_field_valid(new_field), "Field should no longer be valid after removal"

    # Test removing a non-existent field
    assert not fld.remove_field("nonexistent"), "Should not remove a non-existent field"


if __name__ == "__main__":
    pytest.main()
