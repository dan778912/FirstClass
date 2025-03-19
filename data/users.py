import data.db_connect as db
import data.people as ppl
import data.roles as rls
from werkzeug.security import generate_password_hash, check_password_hash
"""
This module interfaces to our user data.
"""

""" For now, I'm just going to use this for creating a basic log-in
    functionality"""

# LEVEL = 'level'
# MIN_USER_NAME_LEN = 2


class AuthError(Exception):
    pass
    # can probably make this cool at some point


def create_user(email: str, password: str) -> dict:
    """
    Create a new user account. User must exist in people database.
    """
    # Check if person exists in people database
    person = ppl.read_one(email)
    if not person:
        raise AuthError("Email not found in people database")

    # Validate roles
    person_roles = person.get("roles", [])
    for role in person_roles:
        if not rls.is_valid(role):
            raise AuthError(f"Invalid role found: {role}")

    # Check if user already exists
    existing = db.get_one("users", {"email": email})
    if existing:
        raise AuthError("User already exists")

    # Create new user
    user = {
        "email": email,
        "password": generate_password_hash(password),
        "roles": person_roles
    }

    db.create("users", user)
    return {
        "email": user["email"],
        "roles": user["roles"]
    }


def authenticate_user(email: str, password: str) -> dict:
    """
    Authenticate a user and return their info if successful.
    """
    user = db.get_one("users", {"email": email})
    if not user or not check_password_hash(user["password"], password):
        raise AuthError("Invalid email or password")

    return {
        "email": user["email"],
        "roles": user["roles"]
    }


def get_user(email: str) -> dict:
    """
    Get user info by email.
    """
    user = db.get_one("users", {"email": email})
    if not user:
        return None
    return {
        "email": user["email"],
        "roles": user["roles"]
    }


def has_role(user: dict, required_roles: list) -> bool:
    """
    Check if user has any of the required roles.
    """
    if not user or not user.get("roles"):
        return False
    return any(role in user["roles"] for role in required_roles)


def delete_users():
    pass
    # delete user from database


def update_users():
    pass
    # update user in database including email and password or access

# def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    # users = {
    #     "Callahan": {
    #         LEVEL: 0,
    #     },
    #     "Reddy": {
    #         LEVEL: 1,
    #     },
    # }
    # get users from database
