from app.member.book_appointment.models.appointment import Appointment

def fetch_all_appointments():
    """
    Fetch all appointments from the database.
    """
    return Appointment.query.order_by(Appointment.id.desc()).all()

