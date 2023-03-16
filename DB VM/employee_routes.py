"""
#
# employee_routes.py contains the python program to define the routes for the application 
# This file is for defining routes in the Database VM
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules and Libraries
# 
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

# employee_database is defined in employee_database.py file

from employee_database import (
    add_employee,
    delete_employee,
    retrieve_employee,
    retrieve_employees,
    update_employee,
)
from employee_models import (
    ErrorResponseModel,
    ResponseModel,
    EmployeeSchema,
    UpdateEmployeeSchema,
)

# Defining the router
router = APIRouter()

# Router for POST operation. 
@router.post("/", status_code=201, response_description="Successfully added employee record into the database") # Defining the post router
async def add_employee_data(employee: EmployeeSchema = Body(...)): # Function to handle the operation
    employee = jsonable_encoder(employee)
    new_employee = await add_employee(employee) # Calling on the add_employee function defined in the employee_database.py file
    return ResponseModel(new_employee, "Employee added successfully.")


# Router for GET operation. Returns the list of all employee records
@router.get("/", status_code=200, response_description="Employees retrieved")
async def get_employees():
    employees = await retrieve_employees() # Calling on the retrieve_employees function defined in the employee_database.py file
    if employees:
        return ResponseModel(employees, "Employees data retrieved successfully")
    return ResponseModel(employees, "Empty list returned")

# Router for GET operation. Returns the record for a single employee
@router.get("/{id}", status_code=200, response_description="Employee data retrieved")
async def get_employee_data(id: int):
    employee = await retrieve_employee(id) # Calling on the retrieve_employee function defined in the employee_database.py file
    if employee:
        return ResponseModel(employee, "Employee data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Employee doesn't exist.")

# Router for PUT operation. Updates the record for a single employee
@router.put("/{id}", status_code=200, response_description="Successfully updated employee record")
async def update_employee_data(id: int, req: UpdateEmployeeSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_employee = await update_employee(id, req) # Calling on the update_employee function defined in the employee_database.py file
    if updated_employee:
        return ResponseModel(
            "Employee with ID: {} name update is successful".format(id),
            "Employee name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the employee data.",
    )

# Router for DELETE operation. Deletes the record for a single employee
@router.delete("/{id}", status_code=200, response_description="Employee data deleted from the database")
async def delete_employee_data(id: int):
    deleted_employee = await delete_employee(id) # Calling on the delete_employee function defined in the employee_database.py file
    if deleted_employee:
        return ResponseModel(
            "Employee with ID: {} removed".format(id), "Employee deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Employee with id {0} doesn't exist".format(id)
    )
