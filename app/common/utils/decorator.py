from functools import wraps

from flask import current_app, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


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
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({"error": "Unauthorized. Insufficient role."}), 403

            return fn(*args, **kwargs)

        return decorated

    return wrapper


def feature_flag_required(flag_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_app.config["FEATURE_FLAGS"].get(flag_name, False):
                return jsonify({"message": f"{flag_name} is temporarily disabled"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
