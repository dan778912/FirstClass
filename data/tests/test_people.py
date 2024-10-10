# test_people.py
import data.people as ppl
import pytest

ADD_EMAIL = "callahan@nyu.edu"

def test_get_people():
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person

def test_create_person():
    people = ppl.get_people()
    assert ADD_EMAIL not in people
    created_person = ppl.create_person("Professor Callahan", "NYU", ADD_EMAIL)
    people = ppl.get_people()
    assert ADD_EMAIL in people
    assert created_person == people[ADD_EMAIL]

# Additional tests for debugging
def test_read_person():
    person = ppl.read_person(ppl.TEST_EMAIL)
    assert person is not None
    assert person[ppl.NAME] == "Alex Martin"

def test_update_person():
    ppl.create_person("Update Test", "NYU", "updatetest@nyu.edu")
    updated_person = ppl.update_person("updatetest@nyu.edu", name="Updated Name")
    assert updated_person["name"] == "Updated Name"

def test_delete_person():
    ppl.create_person("Delete Test", "NYU", "deletetest@nyu.edu")
    assert ppl.delete_person("deletetest@nyu.edu")
    assert ppl.read_person("deletetest@nyu.edu") is None
