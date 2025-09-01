from app.admin.repositories.department_repository import (
    create_department_record,
    find_department_by_name,
    get_all_departments,
)


def create_department_service(data):
    name = data.get("name")
    if not name:
        return {"message": "Department name is required"}, 400

    if find_department_by_name(name):
        return {"message": "Department already exists"}, 409

    create_department_record(name)
    return {"message": "Department created"}, 201


def list_departments_service():
    departments = get_all_departments()
    data = [{"id": d.id, "name": d.name} for d in departments]
    return {"data": data}, 200
