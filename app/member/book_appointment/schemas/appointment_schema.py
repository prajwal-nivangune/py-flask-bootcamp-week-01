from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from app.member.book_appointment.models.appointment import AppointmentStatus


class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(required=True)
    member_id = fields.Int(dump_only=True)
    availability_id = fields.Int(required=True)
    status = EnumField(AppointmentStatus, by_value=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
