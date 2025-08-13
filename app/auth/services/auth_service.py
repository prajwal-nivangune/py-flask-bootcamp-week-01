from app.repositories.user_repository import create_user, find_user_by_email
from app.common.utils.JWT_utils import generate_token


def register_user(data):
    """
    Validate the data and register the user
    :param data:
    :return:
    """
    name = data.get("name")
    email = data.get("email").strip().lower()
    password = data.get("password")
    role = data.get("role")

    if role not in ["doctor", "member"]:
        return {"message": "Invalid role"}, 400

    if find_user_by_email(email):
        return {"message": "Email already registered"}, 409

    create_user(name, email, password, role)
    return {"message": "User created successfully"}, 201

def login_user(data):
    email = data.get("email").strip().lower()
    password = data.get("password")

    user = find_user_by_email(email)

    if not user or not user.check_password(password):
        return {"message": "Invalid password"}, 401

    access_token = generate_token(user.id, user.role)
    return {"access_token": access_token}, 200