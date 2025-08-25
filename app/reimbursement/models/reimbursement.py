import enum
from app.config.db import db
from datetime import datetime

class ClaimStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Reimbursement(db.Model):
    __tablename__ = "reimbursements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(ClaimStatus), default=ClaimStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship("User", backref="reimbursements")
    appointment = db.relationship("Appointment", backref="reimbursements")
