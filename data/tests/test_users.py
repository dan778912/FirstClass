import data.users as usrs
import pytest

NEW_USER_EMAIL = "newuser@nyu.edu"


@pytest.mark.skip(reason="Still figuring out user/login")
def test_get_user():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # checks if one user is created
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)
