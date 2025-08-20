from marshmallow import Schema, fields, validate

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(required=True)
    member_id = fields.Int(dump_only=True)
    availability_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(["booked", "cancelled", "completed"]), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    #TODO
    #enum