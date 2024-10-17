# test_people.py
import data.people as ppl
# import pytest - this line was giving me unused error so i just commented out


ADD_EMAIL = "callahan@nyu.edu"


def test_get_people():
    """
    This is a test to ensure the function `get_people()` is running correctly.
    Checks to ensure people is a dict type, not empty, _id is str type, and
    NAME is in the dict.
    """
    people = ppl.get()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_create_person():
    """
    This is a test to ensure the function `create_person()` is correct.
    Checks to ensure ADD_EMAIL is in people after it is added (and not before).
    """
    people = ppl.get()
    assert ADD_EMAIL not in people
    created_person = ppl.create("Professor Callahan", "NYU", ADD_EMAIL)
    people = ppl.get()
    assert ADD_EMAIL in people
    assert created_person == people[ADD_EMAIL]


def test_read_person():
    """
    This is a test to ensure the function `read_person()` is running correctly.
    Checks to make sure person is not None and name for person is corrrect.
    """
    person = ppl.read(ppl.TEST_EMAIL)
    assert person is not None
    assert person[ppl.NAME] == "Alex Martin"


def test_update_person():
    """
    This is a test to ensure the function `update_person()` is working.
    Checks to see if the name was updated after calling `update_person()`.
    """
    ppl.create("Update Test", "NYU", "updatetest@nyu.edu")
    updated_person = ppl.update("updatetest@nyu.edu",
                                       name="Updated Name")
    assert updated_person["name"] == "Updated Name"


def test_delete_person():
    """
    This is a test to ensure the function `delete_person()` is working.
    Checks to see if person is removed after deleting it.
    """
    ppl.create("Delete Test", "NYU", "deletetest@nyu.edu")
    assert ppl.delete("deletetest@nyu.edu")
    assert ppl.read("deletetest@nyu.edu") is None
