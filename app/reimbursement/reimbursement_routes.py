from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.utils.decorator import role_required, feature_flag_required
from app.reimbursement.services.reimbursement_services import ReimbursementService
from app.reimbursement.schemas.reimbursement_schemas import (
    ReimbursementCreateSchema,
    ReimbursementResponseSchema,
)

reimbursement_bp = Blueprint("reimbursement", __name__, url_prefix="/reimbursement")


@reimbursement_bp.route("/submit", methods=["POST"])
@jwt_required()
@role_required("member")
@feature_flag_required("submit_claim")
def submit_claim():
    try:
        data = request.get_json() or {}
        errors = ReimbursementCreateSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        user_id = get_jwt_identity()
        try:
            claim = ReimbursementService.submit_claim(
                member_id=user_id,
                appointment_id=data["appointment_id"],
                amount=data["amount"],
                description=data.get("description", ""),
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        return ReimbursementResponseSchema().dump(claim), 201

    except SQLAlchemyError:
        return jsonify({"error": "Database error while submitting claim"}), 500


# Admin reviews claim
@reimbursement_bp.route("/review/<int:claim_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
@feature_flag_required("review_claim")
def review_claim(claim_id):
    try:
        data = request.get_json() or {}
        status = data.get("status")
        if not status:
            return jsonify({"error": "Status is required"}), 400

        claim = ReimbursementService.review_claim(claim_id, status)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    return ReimbursementResponseSchema().dump(claim), 200


# Admin views all claims
@reimbursement_bp.route("/get_all_reimbursement", methods=["GET"])
@jwt_required()
@role_required("admin")
@feature_flag_required("view_all_claims")
def get_all_claims():
    claims = ReimbursementService.get_claims()
    return ReimbursementResponseSchema(many=True).dump(claims), 200
