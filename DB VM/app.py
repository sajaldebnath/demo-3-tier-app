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

app = FastAPI()

app.include_router(EmployeeRouter, tags=["Employee"], prefix="/employee") # Base URI is http://<db_vm>/employee


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}