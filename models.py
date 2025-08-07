from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(Enum(Role), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class DoctorDepartment(db.Model):
    __tablename__ = 'doctor_department'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    doctor = db.relationship('User', backref = 'assignments')
    department = db.relationship('Department', backref = 'assignments')