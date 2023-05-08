from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.employee import Employee

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

@employee_bp.route("", methods=["POST"])
def add_employee():
    request_body = request.get_json()
    new_employee = Employee.from_dict(request_body)

    db.session.add(new_employee)
    db.session.commit()

    return {"id": new_employee.id}, 201

@employee_bp.route("", methods=["GET"])
def get_employees():
    response = []

    all_employees = Employee.query.all()

    for employee in all_employees:
        response.append(employee.to_dict())

    return jsonify(response), 200