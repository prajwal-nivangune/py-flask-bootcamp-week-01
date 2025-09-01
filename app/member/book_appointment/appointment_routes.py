from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.common.utils.decorator import feature_flag_required, role_required
from app.common.utils.JWT_utils import get_current_user
from app.member.book_appointment.models.appointment import AppointmentStatus
from app.member.book_appointment.schemas.appointment_schema import AppointmentSchema
from app.member.book_appointment.services.appointment_service import (
    book_appointment_service,
    update_appointment_status_service,
)

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointment")
appointment_schema = AppointmentSchema()


@appointment_bp.route("/member/book_appointment", methods=["POST"])
@role_required("member")
@feature_flag_required("book_appointment")
def book_appointment():
    try:
        current_user = get_current_user()
        data = appointment_schema.load(request.get_json())
        response, status = book_appointment_service(current_user.id, data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500


@appointment_bp.route("/update-status/<int:appointment_id>", methods=["PUT"])
@jwt_required()
@feature_flag_required("update_appointment_status")
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
        new_status = data.get("status")
        if not new_status:
            return jsonify({"message": "Status is required"}), 400

        try:
            new_status_enum = AppointmentStatus[new_status.upper()]
        except KeyError:
            return jsonify({"message": "Invalid status"}), 400

        ALLOWED_STATUS_BY_ROLE = {
            "member": [AppointmentStatus.CANCELLED],
            "doctor": [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED],
            "admin": list(AppointmentStatus),  # Admin can do any status
        }

        if new_status_enum not in ALLOWED_STATUS_BY_ROLE.get(current_user.role, []):
            return jsonify({"message": "You are not authorized to update to this status"}), 403

        response, status_code = update_appointment_status_service(
            appointment_id, new_status_enum, current_user
        )
        return jsonify(response), status_code

    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500
