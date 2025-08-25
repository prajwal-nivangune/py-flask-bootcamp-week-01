from app.reimbursement.repositories.reimbursement_repository import ReimbursementRepo
from app.member.book_appointment.repositories.appointment_repo import get_appointment_by_id
from app.reimbursement.models import ClaimStatus
from app.member.book_appointment.models.appointment import AppointmentStatus

class ReimbursementService:
    @staticmethod
    def submit_claim(member_id, appointment_id, amount, description):
        appointment = get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.status != AppointmentStatus.CANCELLED:
            raise ValueError("Only cancelled appointments are eligible for reimbursement")
        return ReimbursementRepo.create(member_id, appointment_id, amount, description)

    @staticmethod
    def review_claim(claim_id, status: str):
        try:
            status_enum = ClaimStatus[status.upper()]
        except KeyError:
            raise ValueError("Invalid status. Use APPROVED or REJECTED.")

        if status_enum not in (ClaimStatus.APPROVED, ClaimStatus.REJECTED):
            raise ValueError("Only APPROVED or REJECTED are allowed as review statuses.")

        return ReimbursementRepo.update_status(claim_id, status_enum)

    @staticmethod
    def get_claims():
        return ReimbursementRepo.get_all()
