# test_masthead.py

import data.masthead as mast
from data.people import NAME, EMAIL
# from test_people import temp_person


def test_get_masthead():
    """
    Tests the get_masthead function.
    Ensures that the result is a dictionary and non-empty.
    """
    mh = mast.get_masthead()
    assert isinstance(mh, dict)
    assert len(mh) > 0


def test_create_mh_rec():
    person = {
        NAME: "Jane Doe",
        EMAIL: "jane.doe@nyu.edu",
        "roles": ["Author"],
        "affiliation": "NYU"
    }

    result = mast.create_mh_rec(person)
    assert result[NAME] == "Jane Doe", (
        f"Expected NAME to be 'Jane Doe', got {result[NAME]}")
    assert result[EMAIL] == "jane.doe@nyu.edu", (
        f"Expected EMAIL to be 'jane.doe@nyu.edu', got {result[EMAIL]}")


def test_get_mh_fields():
    flds = mast.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0
