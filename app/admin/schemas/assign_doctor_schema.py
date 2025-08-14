from marshmallow import Schema, fields

class AssignDoctorSchema(Schema):
    doctor_id = fields.Int(required=True)
    department_id = fields.Int(required=True)
