from app.member.book_appointment.models.appointment import Appointment
from app.config.db import db
from app.doctor.availability.models.availability import Availability

def create_appointment(member_id, availability_id):
    """
    Create a new appointment and mark the availability as unavailable.
    Assumes validation has been done in service.
    """
    slot = Availability.query.get(availability_id)

    appointment = Appointment(
        doctor_id=slot.doctor_id,
        member_id=member_id,
        availability_id=availability_id,
        status='booked'
    )

    slot.is_available = False

    db.session.add(appointment)
    db.session.commit()

    return appointment

def get_appointment_by_availability(availability_id):
    return Appointment.query.filter_by(availability_id=availability_id).first()

def get_all_appointments():
    return Appointment.query.order_by(Appointment.id.desc()).all()

def get_appointments_by_doctor(doctor_id):
    return Appointment.query.filter_by(doctor_id=doctor_id).all()

def update_appointment_status(appointment_id, status):
    """
    Update the status of an existing appointment.
    """
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return None, "Appointment not found"

    appointment.status = status
    db.session.commit()
    return appointment, None

