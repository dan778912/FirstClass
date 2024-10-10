import data.people as ppl


def test_get_people():
    """
    Test function for get_people.
    Checks to ensure that people is type dict, and length > 0.
    Checks to ensure that id in dict are type string,

    """
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


ADD_EMAIL = "callahan@nyu.edu"


def test_create_person():
    people = ppl.get_people
    assert ADD_EMAIL not in people
    ppl.create_person("Professor Callahan", "NYU", ADD_EMAIL)
    people = ppl.get_people()
    assert ADD_EMAIL in people