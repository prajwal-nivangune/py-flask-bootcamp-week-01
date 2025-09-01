from sqlalchemy.exc import SQLAlchemyError

from app.common.models import User
from app.config.db import db


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def commit_changes():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


def find_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def create_user(name, email, password, role):
    """
    Add a new user to the database
    :param name:
    :param email:
    :param password:
    :param role:
    :return:
    """
    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    # db.session.commit()
    commit_changes()
    return user
