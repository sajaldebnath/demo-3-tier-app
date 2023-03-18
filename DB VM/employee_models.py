"""
#
# employee_models.py contains the python program to define the models for Database schema
# This file is for defining schema/models for collection in the MongoDB database
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules and Libraries
# 
from typing import Optional
from pydantic import BaseModel, EmailStr, Field # Pydantic is needed for validation and data serialization


# Defining the Employee schema. Entries here matches with the Database collection structure 
# Since it is mongodb so no strict table schema is needed, but the strucuture needs to be defined here to map the fields
class EmployeeSchema(BaseModel):
    emp_id: int = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    ph_no: str = Field(...)
    home_addr: str = Field(...) 
    st_addr: str = Field(...)
    gender: str = Field(...)
    job_type: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Blanch",
                "last_name": "Nolin",
                "email": "Blanch.Nolin@acme.com",
                "ph_no": "192-573-4906",
                "home_addr": "PO Box 18746",
                "st_addr": "2 Hallows Street",
                "gender": "Female",
                "job_type":"Senior Cost Accountant"
            }
        }


class UpdateEmployeeSchema(BaseModel):
    emp_id: int = Field(...)
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    ph_no: Optional[str]
    home_addr: Optional[str]
    st_addr: Optional[str]
    gender: Optional[str]
    job_type: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first_name":"Frieda",
                "last_name":"Harman",
                "email":"Frieda.Harman@acme.com",
                "ph_no":"591-892-1118",
                "home_addr":"15th Floor",
                "st_addr":"2 Dayton Circle",
                "gender":"Female",
                "job_type":"Staff Scientist"
            }
        }


def ResponseModel(data, code, message):
    return {
        "data": [data],
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
