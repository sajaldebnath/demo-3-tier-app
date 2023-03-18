"""
#
# employee_database.py contains the python program to define the database operations for the application 
# This file is for defining access methods of database and operations on database
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules and Libraries
# 
import asyncio
import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://localhost:27017"  # Asssuming mongodb is running in local server. Change for a remote DB server

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS) # Defining the database access client

database = client.employees_DB # Connecting to the employee_DB database. Change the database name for connecting to another database

employee_collection = database.get_collection("employees") # Getting the employees collection. Change the collection name to connect to another


# helpers
# Changing the data to python dictionary. Note, the changing of the id as string from bson ObjectId (mongodb)
def employee_helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "emp_id": employee["emp_id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "email": employee["email"],
        "ph_no": employee["ph_no"],
        "home_addr": employee["home_addr"],
        "st_addr": employee["st_addr"],
        "gender": employee["gender"],
        "job_type": employee["job_type"],
    }



# Retrieve all employees present in the database
async def retrieve_employees():
    employees = []
    async for employee in employee_collection.find():
        employees.append(employee_helper(employee))
    return employees


# Add a new employee into to the database
async def add_employee(employee_data: dict) -> dict:
    employee = await employee_collection.insert_one(employee_data)
    new_employee = await employee_collection.find_one({"_id": employee.inserted_id})
    return employee_helper(new_employee)


# Retrieve an employee with a matching employee ID
async def retrieve_employee(emp_id: int) -> dict:
    employee = await employee_collection.find_one({"emp_id": emp_id})
    if employee:
        return employee_helper(employee)


# Update an employee with a matching employee ID
async def update_employee(emp_id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    employee = await employee_collection.find_one({"emp_id": emp_id})
    if employee:
        updated_employee = await employee_collection.update_one(
            {"emp_id": emp_id}, {"$set": data}
        )
        if updated_employee:
            return True
        return False


# Delete an employee from the database
async def delete_employee(emp_id: int):
    employee = await employee_collection.find_one({"emp_id": emp_id }) # ObjectId(id)})
    if employee:
        await employee_collection.delete_one({"emp_id": emp_id }) #ObjectId(id)})
        return True
