from contextlib import contextmanager
from datetime import date
from typing import Generator, Optional
import connexion.lifecycle  # type: ignore
from flask import g, request
import pydantic
from sqlalchemy.orm import Session
from sqlalchemy import text
import connexion  # type: ignore
# from connexion import lifecycle, request

# from backend_engineer_interview.models import Employee
from backend_engineer_interview.db import SQLDatabaseManager


class PydanticBaseModel(pydantic.BaseModel):
    model_config = {"from_attributes": True}


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Get a plain SQLAlchemy Session."""
    session: Optional[Session] = g.get("db")
    if session is None:
        raise Exception("No database session available in application context")

    yield session


def get_request() -> connexion.lifecycle.ConnexionRequest:
    return connexion.request


def status() -> tuple[dict, int, dict]:
    with db_session() as session:
        session.execute(text("SELECT 1;")).one()
        return ({"status": "up"}, 200, {})


class EmployeeResponse(PydanticBaseModel):
    model_config = {"from_attributes": True}

    id: int
    first_name: str
    last_name: str
    date_of_birth: date


sql_instance = SQLDatabaseManager(db_session=db_session)


def get_employee(id: int) -> None:
    # ANSWER
    employee = sql_instance.get_employee_by_id(id, ['secret'])
    if employee:
        return employee, 200
    return {'message': 'No such employee'}, 404 


def patch_employee(id: int, body: dict) -> None:
    # ANSWER
    errorMessage = ''
    last_name = body.get('last_name')
    first_name = body.get('first_name')
    if last_name == "":
        errorMessage = "last_name cannot be blank"
    if first_name == "":
        errorMessage = f"{errorMessage};first_name cannot be blank"
    if errorMessage:
        return {'message': errorMessage}, 400
    updated_employee = sql_instance.update_employee(id, first_name=first_name, last_name=last_name)
    if updated_employee:
        return updated_employee, 204
    return {'message': 'No such employee'}, 404


def post_application(body: dict) -> None:
    """
    Accepts a leave_start_date, leave_end_date, employee_id and creates an Application
    with those properties.  It should then return the new application with a status code of 200.

    If any of the properties are missing in the request body, it should return the new application
    with a status code of 400.

    Verify the handler using the test cases in TestPostApplication.  Add any more tests you think
    are necessary.
    """
    # Answer
    errorMessage = ''
    if body:
        employee_id = body.get('employee_id')
        leave_start_date = body.get('leave_start_date')
        leave_end_date = body.get('leave_end_date')
        if employee_id and leave_start_date and leave_end_date:
            new_application = sql_instance.create_leave_application(employee_id=employee_id, leave_start_date=leave_start_date, leave_end_date=leave_end_date)
            if new_application:
                return new_application, 200
        if not employee_id:
            errorMessage = 'employee_id is missing;'
        if not leave_start_date:
            errorMessage = f'{errorMessage}leave_start_date is missing;'
        if not leave_start_date:
            errorMessage = f'{errorMessage}leave_end_date is missing'
    return {'message': errorMessage}, 400


def search_application() -> None:
    """
    Returns a list of applications.  Can provide an employee id, first name or last name to filter the results
    """
    # Answer
    query_params = request.args
    page = query_params.get('page')
    employee_id = query_params.get('employee_id')
    first_name = query_params.get('first_name')
    last_name = query_params.get('last_name')

    return sql_instance.search_leave_applications(employee_id=employee_id, first_name=first_name, last_name=last_name, page=page), 200
