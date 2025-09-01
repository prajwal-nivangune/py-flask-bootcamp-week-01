from sqlalchemy.exc import SQLAlchemyError

from app.admin.models import Department
from app.config.db import db


def find_department_by_name(name):
    return Department.query.filter_by(name=name).first()


def find_department_by_id(department_id):
    return Department.query.filter_by(id=department_id).first()


def get_all_departments():
    return Department.query.all()


def create_department_record(name):
    dept = Department(name=name)
    db.session.add(dept)
    try:
        db.session.commit()
        return {"message": "Department created"}, 201
    except SQLAlchemyError:
        db.session.rollback()
        raise
