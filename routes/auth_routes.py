from flask import jsonify, Blueprint, request
from models import User, db
from utils.JWT_utils import generate_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/auth/register", methods = ["POST"])
def register():
    """
    Register a new user
    :return:
    """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email").strip().lower()
    password = data.get("password")
    role = data.get("role")

    if role not in ["doctor", "member"]:
        return jsonify({"message" : "Invalid role"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message" : "User Register Successfully"}), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Login a user
    :return:
    """
    data = request.get_json()
    email = data.get("email").strip().lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message" : "Invalid password"}), 401

    access_token = generate_token(user.id, user.role)
    return jsonify({"access_token" : access_token}), 200
