from app.config.db import db


class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)

    doctor = db.relationship("User", backref="availability")

    __table_args__ = (db.UniqueConstraint("doctor_id", "start_time", name="uq_doctor_start_time"),)

    def serialize(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "is_available": self.is_available,
        }
