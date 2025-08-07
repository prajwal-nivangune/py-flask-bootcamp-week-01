from flask import Blueprint, request, jsonify
from utils.decorator import admin_required
from models import User, Department, DoctorDepartment, db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/departments',methods = ["POST"])
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

@admin_bp.route('/departments',methods = ["GET"])
@admin_required
def list_departments():
    """
    admin required to list the Departments
    :return:
    """
    departments = Department.query.all()
    data = [{"id" : d.id, "name" : d.name  } for d in departments]
    return jsonify({"data" : data}), 200


@admin_bp.route('/doctors',methods = ["POST"])
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


@admin_bp.route('/assign-doctor', methods=['POST'])
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

