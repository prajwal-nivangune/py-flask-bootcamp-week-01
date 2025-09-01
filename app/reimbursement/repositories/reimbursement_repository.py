from app import db
from app.reimbursement.models import ClaimStatus, Reimbursement


class ReimbursementRepo:
    @staticmethod
    def create(member_id, appointment_id, amount, description):
        claim = Reimbursement(
            member_id=member_id,
            appointment_id=appointment_id,
            amount=amount,
            description=description,
        )
        db.session.add(claim)
        db.session.commit()
        return claim

    @staticmethod
    def get_by_id(claim_id):
        return Reimbursement.query.get(claim_id)

    @staticmethod
    def get_all():
        return Reimbursement.query.all()

    @staticmethod
    def update_status(claim_id, status: ClaimStatus):
        claim = Reimbursement.query.get(claim_id)
        if claim:
            claim.status = status
            db.session.commit()
        return claim
