from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.auth.services.auth_service import register_user, login_user
from marshmallow import ValidationError
from app.common.schemas.user_schema import UserSchema
from app.common.schemas.login_schema import LoginSchema

user_schema = UserSchema()
login_schema = LoginSchema()

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/auth/register", methods = ["POST"])
def register():
    """
    Register a new User in the system

    :return:
    """
    try:
        data = user_schema.load(request.get_json())
        response, status = register_user(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500

@auth_bp.route("/auth/login", methods = ["POST"])
def login():
    try:
        data = login_schema.load(request.get_json())
        response, status = login_user(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500