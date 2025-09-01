from marshmallow import Schema, fields, validate


class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=[validate.Length(min=3, max=100)],
        error_messages={
            "required": "Department name is required",
            "null": "Department name can not be  null",
        },
    )
