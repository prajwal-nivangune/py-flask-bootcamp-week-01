from marshmallow import Schema, fields


class AvailabilitySchema(Schema):
    id = fields.Integer(dump_only=True)
    doctor_id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    is_available = fields.Boolean()
