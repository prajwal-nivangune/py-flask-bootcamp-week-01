from app.admin.repositories.appointment_repository import fetch_all_appointments

def get_all_appointments_service():
    """
    Fetch all appointments and format the data for admin.
    """
    appointments = fetch_all_appointments()
    result = []

    for a in appointments:
        result.append({
            "id": a.id,
            "doctor_id": a.doctor_id,
            "member_id": a.member_id,
            "availability_id": a.availability_id,
            "status": a.status,
            "created_at": a.created_at.isoformat()
        })

    return result
