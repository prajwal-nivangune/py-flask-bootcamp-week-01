from sqlalchemy.exc import SQLAlchemyError

from app.admin.models import DoctorDepartment
from app.config.db import db


def find_assignment(doctor_id, department_id):
    return DoctorDepartment.query.filter_by(
        doctor_id=doctor_id, department_id=department_id
    ).first()


def create_assignment(doctor_id, department_id):
    assignment = DoctorDepartment(doctor_id=doctor_id, department_id=department_id)
    db.session.add(assignment)
    try:
        db.session.commit()
        return assignment
    except SQLAlchemyError:
        db.session.rollback()
        raise
