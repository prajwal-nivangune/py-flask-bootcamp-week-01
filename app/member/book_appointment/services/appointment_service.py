from app.member.book_appointment.repositories.appointment_repo import create_appointment, get_appointment_by_availability, update_appointment_status
from app.doctor.availability.models.availability import Availability

def book_appointment_service(member_id, data):
    availability_id = data.get('availability_id')
    if not availability_id:
        return {"message": "availability_id is required"}, 400

    slot = Availability.query.get(availability_id)
    if not slot or not slot.is_available:
        return {"message": "Slot not available"}, 400

    existing = get_appointment_by_availability(availability_id)
    if existing:
        return {"message": "Slot already booked"}, 400

    appointment = create_appointment(member_id, availability_id)

    return {
        "message": "Appointment booked successfully",
        "appointment": {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "member_id": appointment.member_id,
            "availability_id": appointment.availability_id,
            "status": appointment.status,
            "created_at": appointment.created_at.isoformat()
        }
    }, 201

def update_appointment_status_service(appointment_id, status, current_user):
    """
    Validate and update the appointment status.
    """
    if status not in ["booked", "cancelled", "completed"]:
        return {"message": "Invalid status"}, 400

    appointment, error = update_appointment_status(appointment_id, status)
    if error:
        return {"message": error}, 404

    if current_user.role == "member" and appointment.member_id != current_user.id:
        return {"message": "You cannot update someone else's appointment"}, 403
    elif current_user.role == "doctor" and appointment.doctor_id != current_user.id:
        return {"message": "You cannot update another doctor's appointment"}, 403

    return {
        "message": "Appointment status updated successfully",
        "appointment": {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "member_id": appointment.member_id,
            "availability_id": appointment.availability_id,
            "status": appointment.status,
            "created_at": appointment.created_at.isoformat()
        }
    }, 200
