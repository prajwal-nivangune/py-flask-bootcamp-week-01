from flask import Blueprint, request ,jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.utils.decorator import admin_required
from app.services.admin_service import promote_user_service, onboard_doctor_service, assign_doctor_service
from app.services.department_service import create_department_service, list_departments_service

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/promote-user/<int:user_id>', methods=['PUT'])
@admin_required
def promote_user(user_id):
    try:
        response, status = promote_user_service(user_id)
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/create-department', methods=['POST'])
@admin_required
def create_department():
    try:
        data = request.get_json()
        response,status = create_department_service(data)
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/departments',methods = ["GET"])
@admin_required
def list_departments():
    try:
        response,status = list_departments_service()
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/doctors', methods = ["POST"])
@admin_required
def onboard_doctor():
    try:
        data = request.get_json()
        response, status = onboard_doctor_service(data)
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@admin_bp.route('/assign-doctor', methods=['POST'])
@admin_required
def assign_doctor():
    try:
        data = request.get_json()
        response,status = assign_doctor_service(data)
        return jsonify(response), status
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500



