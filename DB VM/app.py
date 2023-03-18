#!/usr/bin python3

"""
#
# app.py contains the python program to define the application  
# This file is for defining main application in the Database VM
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules and Libraries
# 
from fastapi import FastAPI
from employee_routes import router as EmployeeRouter  # Importing the routes


description = """
Emnployee Database API exposes the employee database to the outside world through REST API CRUD operations.
This is part of a demo 3-tier application which mimics a real life application albeit in much simplistic way.
Since the services are exposed using CRUD operations, it is very easy to change the actual database. Till the time
schema does not change it does not impact rest of the application. Just replace the database and change the access
method in whatever programming language you are using.
Also, this way front end and mid-tier logic is completely separated from backend database. 

## Records

You can **create records**.
You can **read records**.
You can **update records**.
You can **delete records**.

## Users

You will be able to:

* **Rolse based access control** (_not implemented_).

"""


app = FastAPI(
    title="EmployeeDatabase",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Sajal Debnath",
        "url": "https://sajaldebnath.com",
        "email": "sdebnath@vmware.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/",
    },
)

app.include_router(EmployeeRouter, tags=["Employee"], prefix="/employee") # Base URI is http://<db_vm>/employee


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}