from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.common.utils.decorator import doctor_required
from app.common.utils.JWT_utils import get_current_user
from app.doctor.availability.schemas.availability_schema import AvailabilitySchema
from app.doctor.availability.services.availability_service import create_availability_slot, get_availability_slot

availability_bp = Blueprint('availability_bp', __name__)
availability_schema = AvailabilitySchema()

@availability_bp.route('/doctor/create-availability', methods=['POST'])
@doctor_required
def create_availability():
    try:
        current_user = get_current_user()
        data = availability_schema.load(request.get_json())
        response, status = create_availability_slot(current_user, data)
        return jsonify(response), status
    except ValidationError as e:
        return jsonify(e.messages), 400
    except SQLAlchemyError:
        return jsonify({'message': 'Something went wrong'}), 500

@availability_bp.route('/doctor/get-availability', methods=['GET'])
@doctor_required
def get_availability():
    try:
        current_user = get_current_user()
        print(current_user)
        response, status = get_availability_slot(current_user)
        print(response)
        return jsonify(response), status
    except SQLAlchemyError as e:
        return jsonify({"message": f"Something went wrong {e}"}), 500