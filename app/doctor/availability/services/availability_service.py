from app.doctor.availability.repositories.availability_repository import create_slot,get_slots_by_doctor, get_availability_by_id, save_availability

def create_availability_slot(current_user, data):
    if current_user.role != 'doctor':
        return {"message" : "Only doctors can create availability"}, 403
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    slot = create_slot(current_user.id, start_time, end_time)
    return {"message": "Availability created", "id": slot.id}, 201

def get_availability_slot(current_user):
    slots = get_slots_by_doctor(current_user.id)
    return [s.serialize() for s in slots], 200

def update_availability_service(current_user, availability_id, data):
    slot = get_availability_by_id(availability_id)
    if not slot:
        return {"message": "Availability slot not found"}, 404

    if slot.doctor_id != current_user.id:
        return {"message": "You cannot update another doctor's availability"}, 403

    if "start_time" in data:
        slot.start_time = data["start_time"]
    if "end_time" in data:
        slot.end_time = data["end_time"]
    if "is_available" in data:
        slot.is_available = data["is_available"]

    save_availability(slot)

    return {
        "message": "Availability updated successfully",
        "availability": slot.serialize()
    }, 200
