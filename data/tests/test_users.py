import data.users as usrs


def test_get_users():
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

def test_create_user():
    users = usrs.get_users()
    assert NEW_USER_EMAIL not in users
    new_user = usrs.create_user("New User", NEW_USER_EMAIL, 1)
    users = usrs.get_users()
    assert NEW_USER_EMAIL in users
    assert new_user == users[NEW_USER_EMAIL]

