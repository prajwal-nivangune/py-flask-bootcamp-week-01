from flask import Blueprint, request ,jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from app.common.utils.decorator import feature_flag_required, role_required
from app.admin.services.admin_service import promote_user_service, onboard_doctor_service, assign_doctor_service
from app.admin.services.department_service import create_department_service, list_departments_service
from app.admin.services.appointment_service import get_all_appointments_service
from app.admin.schemas.department_schema import DepartmentSchema
from app.admin.schemas.assign_doctor_schema import AssignDoctorSchema
from app.admin.schemas.onboard_doctor_schema import OnboardDoctorSchema
from marshmallow import ValidationError

department_schema = DepartmentSchema()
onboard_doctor_schema = OnboardDoctorSchema()
assign_doctor_schema = AssignDoctorSchema()

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/promote-user/<int:user_id>', methods=['PUT'])
@role_required('admin')
@feature_flag_required("promote_user")
def promote_user(user_id):
    """Promote a user to a higher role."""
    try:
        response, status = promote_user_service(user_id)
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/create-department', methods=['POST'])
@role_required('admin')
@feature_flag_required("create_department")
def create_department():
    """Create a new department."""
    try:
        data = department_schema.load(request.get_json())
        response,status = create_department_service(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/departments',methods = ["GET"])
@role_required('admin')
@feature_flag_required("create_department")
def list_departments():
    """List all departments."""
    try:
        response,status = list_departments_service()
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/doctors', methods = ["POST"])
@role_required('admin')
@feature_flag_required("onboard_doctor")
def onboard_doctor():
    """Create a new doctor."""
    try:
        data = onboard_doctor_schema.load(request.get_json())
        response, status = onboard_doctor_service(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/assign-doctor', methods=['POST'])
@role_required('admin')
@feature_flag_required("assign_doctor")
def assign_doctor():
    """Assign a doctor to a department."""
    try:
        data = assign_doctor_schema.load(request.get_json())
        response,status = assign_doctor_service(data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required('admin')
@feature_flag_required("view_appointments")
def get_all_appointments():
    try:
        appointments = get_all_appointments_service()
        return jsonify({"appointments": appointments}), 200
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500