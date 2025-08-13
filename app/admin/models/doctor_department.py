from app.config.db import db

class DoctorDepartment(db.Model):
    __tablename__ = 'doctor_department'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    doctor = db.relationship('User', backref = 'assignments')
    department = db.relationship('Department', backref = 'assignments')