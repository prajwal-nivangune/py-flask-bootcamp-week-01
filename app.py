from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from functools import wraps
from models import db, User, Department, DoctorDepartment
from utils.JWT_utils import generate_token
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()



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


@app.route('/departments',methods = ["POST"])
@admin_required
def create_department():
    """
     admin required to create the Department
    :return:
    """
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"message" : "Department name is required"}), 400

    if Department.query.filter_by(name=name).first():
        return jsonify({"message" : "Department already exists"}), 400

    dept = Department(name=name)
    db.session.add(dept)
    db.session.commit()
    return jsonify({"message" : "Department created"}), 201

@app.route('/departments',methods = ["GET"])
@admin_required
def list_departments():
    """
    admin required to list the Departments
    :return:
    """
    departments = Department.query.all()
    data = [{"id" : d.id, "name" : d.name  } for d in departments]
    return jsonify({"data" : data}), 200


@app.route('/doctors',methods = ["POST"])
@admin_required
def onboard_doctor():
    """
    admin required to create the Doctor
    :return:
    """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email").strip().lower()
    password = data.get("password")
    if not all([name, email, password]):
        return jsonify({"message" : "Name, email, and password are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message" : "Doctor already exists"}), 400
    doctor = User(name=name, email=email, role="doctor")
    doctor.set_password(password)
    db.session.add(doctor)
    db.session.commit()
    return jsonify({"message" : "Doctor onboarded"}), 201


@app.route('/assign-doctor', methods=['POST'])
@admin_required
def assign_doctor():
    """
    admin can assign doctor to department
    :return:
    """
    data = request.get_json()
    doctor_id = data.get("doctor_id")
    department_id = data.get("department_id")
    if not all([doctor_id, department_id]):
        return jsonify({"message" : "Doctor ID or Department ID is required"}), 400
    doctor = User.query.filter_by(id=doctor_id).first()
    if not doctor:
        return jsonify({"message" : "Doctor not found"}), 404

    department = Department.query.filter_by(id=department_id).first()
    if not department:
        return jsonify({"message" : "Department not found"}), 404

    if doctor.role != "doctor":
        return jsonify({"message" : "user is not a doctor"}), 400

    if DoctorDepartment.query.filter_by(doctor_id = doctor.id, department_id = department.id).first():
        return jsonify({"message" : "Doctor already assigned to the department"}), 409

    assignment = DoctorDepartment(doctor_id=doctor.id, department_id=department.id)
    db.session.add(assignment)
    db.session.commit()
    return jsonify({"message" : "Doctor assigned to the department"}), 201



@app.route("/auth/register", methods = ["POST"])
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

@app.route("/auth/login", methods=["POST"])
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


@app.route("/")
def index():
    return "RBAC Assignment"

if __name__ == '__main__':
    app.run(debug=True)