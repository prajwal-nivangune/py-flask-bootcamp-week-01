from sqlalchemy.exc import SQLAlchemyError
from app.config.db import db
from app.doctor.availability.models.availability import Availability

def create_slot(doctor_id, start_time, end_time):
    slot = Availability(
        doctor_id=doctor_id,
        start_time=start_time,
        end_time=end_time,
        is_available=True
    )
    db.session.add(slot)
    return _commit(slot)

def get_slots_by_doctor(doctor_id):
    return Availability.query.filter_by(doctor_id=doctor_id).all()

def _commit(instance):
    try:
        db.session.commit()
        return instance
    except SQLAlchemyError:
        db.session.rollback()
        raise
