from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.String(required=True, validate=validate.OneOf(["user", "member", "admin"]))
