from app.doctor.availability.repositories.availability_repository import create_slot,get_slots_by_doctor

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