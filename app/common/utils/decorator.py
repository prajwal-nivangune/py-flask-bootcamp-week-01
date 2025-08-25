from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(func):
    """
    Decorator that checks that the user is an admin
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data["role"] != "admin":
                return jsonify({"message" : "Forbidden"}), 403
        except Exception as e:
            return jsonify({"message" : "Unauthorized", "error": str(e)}), 401
        return func(*args, **kwargs)
    return wrapper

def doctor_required(func):
    """
    Decorator that checks that the user is a doctor
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data["role"] != "doctor":
                return jsonify({"message" : "Forbidden"}), 403
        except Exception as e:
            return jsonify({"message" : "Unauthorized", "error": str(e)}), 401
        return func(*args, **kwargs)
    return wrapper

def member_required(func):
    """
    Decorator that checks that the user is a member
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data["role"] != "member":
                return jsonify({"message" : "Forbidden"}), 403
        except Exception as e:
            return jsonify({"message" : "Unauthorized", "error": str(e)}), 401
        return func(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """
    Restrict route access to specific roles.
    Usage:
    @jwt_required()
    @role_required("admin", "doctor")
    def my_route():
        ...
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({"error": "Unauthorized. Insufficient role."}), 403

            return fn(*args, **kwargs)

        return decorated

    return wrapper