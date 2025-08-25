from app.config.db import db
from datetime import datetime
import enum

class AppointmentStatus(enum.Enum):
    PENDING = "PENDING"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'), nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('User', foreign_keys=[doctor_id])
    member = db.relationship('User', foreign_keys=[member_id])
    availability = db.relationship('Availability', foreign_keys=[availability_id])