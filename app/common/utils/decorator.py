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