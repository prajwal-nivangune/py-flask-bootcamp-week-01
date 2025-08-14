from app.common.repositories import find_user_by_id, commit_changes, find_user_by_email, create_user
from app.admin.repositories.department_repository import find_department_by_id
from app.admin.repositories.doctor_department_repository import find_assignment, create_assignment

def promote_user_service(user_id):
    user = find_user_by_id(user_id)

    if not user:
        return {"message": "User not found"}, 404

    if user.role == 'admin':
        return {"message": "User is already an admin"}, 200

    user.role = 'admin'
    commit_changes()

    return {"message": "User promoted to admin"}, 200

def onboard_doctor_service(data):
    name = data.get("name")
    email = data.get("email").strip().lower()
    password = data.get("password")
    if not all([name, email, password]):
        return {"message": "Name, email, and password are required"}, 400
    if find_user_by_email(email):
        return {"message": "Doctor already exists"}, 400

    create_user(name, email, password, role="doctor")
    return {"message": "Doctor onboarded"}, 201

def assign_doctor_service(data):
    doctor_id = data.get("doctor_id")
    department_id = data.get("department_id")

    if not all([doctor_id, department_id]):
        return {"message": "Doctor ID or Department ID is required"}, 400
    doctor = find_user_by_id(doctor_id)
    if not doctor:
        return {"message": "Doctor not found"}, 404

    department = find_department_by_id(department_id)
    if not department:
        return {"message": "Department not found"}, 404

    if doctor.role != "doctor":
        return {"message": "user is not a doctor"}, 400

    if find_assignment(doctor_id, department_id):
        return {"message": "Doctor already assigned to the department"}, 409

    create_assignment(doctor_id, department_id)
    return {"message": "Doctor assigned to the department"}, 201




