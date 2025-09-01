from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from app.reimbursement.models import ClaimStatus


class ReimbursementCreateSchema(Schema):
    appointment_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(required=False)


class ReimbursementResponseSchema(Schema):
    id = fields.Int()
    member_id = fields.Int()
    appointment_id = fields.Int()
    amount = fields.Float()
    description = fields.Str()
    status = EnumField(ClaimStatus, by_value=True)
    created_at = fields.DateTime()
