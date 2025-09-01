from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.auth.services.auth_service import login_user, register_user
from app.common.schemas.login_schema import LoginSchema
from app.common.schemas.user_schema import UserSchema
from app.common.utils.decorator import feature_flag_required

user_schema = UserSchema()
login_schema = LoginSchema()

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
@feature_flag_required("registration")
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


@auth_bp.route("/auth/login", methods=["POST"])
@feature_flag_required("login")
def login():
    try:
        data = login_schema.load(request.get_json())
        response, status = login_user(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
@feature_flag_required("logout")
def logout():
    jti = get_jwt()["jti"]
    current_app.redis.setex(jti, 3600, "revoked")
    return jsonify({"message": "Logged out successfully"}), 200
