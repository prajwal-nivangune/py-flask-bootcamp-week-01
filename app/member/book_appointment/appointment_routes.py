from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.common.utils.JWT_utils import get_current_user
from app.common.utils.decorator import member_required
from app.member.book_appointment.schemas.appointment_schema import AppointmentSchema
from app.member.book_appointment.services.appointment_service import book_appointment_service, update_appointment_status_service

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointment')
appointment_schema = AppointmentSchema()

@appointment_bp.route('/member/book_appointment', methods=['POST'])
@member_required
def book_appointment():
    try:
        current_user = get_current_user()
        data = appointment_schema.load(request.get_json())
        response, status = book_appointment_service(current_user.id, data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500


@appointment_bp.route('/update-status/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment_status_route(appointment_id):
    """
    Update the status of an appointment.
    Role-based rules:
    - Member: can cancel their own appointment
    - Doctor: can mark completed or cancel their own appointments
    - Admin: can update any status
    """
    try:
        current_user = get_current_user()
        data = request.get_json()
        new_status = data.get('status')
        if not new_status:
            return jsonify({"message": "Status is required"}), 400

        allowed = False
        if current_user.role == "member" and new_status == "cancelled":
            allowed = True
        elif current_user.role == "doctor" and new_status in ["cancelled", "completed"]:
            allowed = True
        elif current_user.role == "admin":
            allowed = True
        #TODO
        #keep it more generic

        if not allowed:
            return jsonify({"message": "You are not authorized to update to this status"}), 403

        response, status_code = update_appointment_status_service(appointment_id, new_status, current_user)
        return jsonify(response), status_code

    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500



