#!/usr/bin python

"""
#
# Program to get data from remote DB server and show in the frontend
# This script defines all the routes to be accessed by frontend web server
# Author Sajal Debnath <sdebnath@vmware.com><debnathsajal@gmail.com>
#
"""
# Importing the Modules
from flask import Flask, render_template, request, jsonify
import requests
# Defining the Database details
import time
import json


db_fqdn = "10.123.10.187"  # Modify the value with the actual database server
api_url_base = "http://" + db_fqdn + "/employee"

# Defining the app details
# Init app
app = Flask(__name__)

app.config["DEBUG"] = True

################### Define functions and routes ##########################

# Get all the employees data
@app.route('/')
def employees():#
    api_url = "{0}".format(api_url_base)

    response = ''
    while response == '':
        try:
            response = requests.get(api_url, headers=header, verify=False)
            break
        except:
            for i in range(3):
                print("Connection refused by the server..")
                print("Let's wait for 5 seconds and try again")
                time.sleep(5)
                print("Trying again...")
                continue
    
    #print(response)
    if response.status_code == 200:
         json_data_all = response.json()
         json_data = json_data_all["data"]
         employee_data = json_data[0]
         #print(json_data[0])
         return render_template('homepage.html',employee_data=employee_data)
    else:
         print("Could not get employee list")
         return "Could not get employee list"


# Create a new employee record
@app.route('/employee', methods=["POST"]) #,"GET"])  
def single_employee():
    api_url = "{0}".format(api_url_base)
    headers = {'content-type': 'application/json'}

    if request.method == 'POST':
        emp_id = request.form['emp_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        #email = first_name + '.' + last_name + 'acme.com'  # Email auto-generated
        email = request.form['email']
        ph_no = request.form['ph_no']
        home_addr = request.form['home_addr']
        st_addr = request.form['st_addr']
        gender = request.form['gender']
        job_type = request.form['job_type']
        # print(emp_id)
        # print(first_name)
        # print(last_name)
        # print(email)
        # print(ph_no)
        # print(home_addr)
        # print(st_addr)
        # print(gender)
        # print(job_type)
        # print("I am making the request now")
        request_body = {
            "emp_id": emp_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "ph_no": ph_no,
            "home_addr": home_addr,
            "st_addr": st_addr,
            "gender": gender,
            "job_type": job_type
            }
        
        #payload = jsonify(request_body)
        print("Request Body", request_body)
        
        response = ''
        while response == '':
            try:
                response = requests.post(api_url, data = json.dumps(request_body), headers=headers)
                break
            except:
                for i in range(3):
                    print("Connection refused by the server..")
                    print("Let's wait for 5 seconds and try again")
                    time.sleep(5)
                    print("Trying again...")
                    continue
        
        #print(response)
        
        info=response.json()
        #print(info)


        #print(response.status_code)
        if response.status_code == 201:
            json_data_all = response.json()
            json_data = json_data_all["data"]

            print("Successfully added the record for the employee: {}".format(first_name))
            return ("Successfully added the record for the employee: {}".format(first_name))
        else:
            print("Could not add to the employee record. Error: {}".format(info))
            
            return ("Could not add to the employee record. Error: {}".format(info))


# GET, UPDATE/Edit, DELETE an existing employee record
@app.route('/employee/<int:id>', methods=["PUT","GET", "DELETE"])
def edit_employee_record(id):
    api_url = "{0}/{1}".format(api_url_base, id)
    headers = {'content-type': 'application/json'}
    # response = requests.get(api_url, headers=header, verify=False)

    if request.method == 'PUT':
        emp_id = request.form['emp_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = first_name + '.' + last_name + '@acme.com'  # Email auto-generated
        ph_no = request.form['ph_no']
        home_addr = request.form['home_addr']
        st_addr = request.form['st_addr']
        gender = request.form['gender']
        job_type = request.form['job_type']
        # print(emp_id)
        # print(first_name)
        # print(last_name)
        # print(email)
        # print(ph_no)
        # print(home_addr)
        # print(st_addr)
        # print(gender)
        # print(job_type)
        # print("I am making the edit request now")
        request_body = {
            "emp_id": emp_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "ph_no": ph_no,
            "home_addr": home_addr,
            "st_addr": st_addr,
            "gender": gender,
            "job_type": job_type
            }
        
        #payload = jsonify(request_body)
        print("Request Body", request_body)
        response = ''
        while response == '':
            try:
                response = requests.put(api_url, data = json.dumps(request_body), headers=headers)
                break
            except:
                for i in range(3):
                    print("Connection refused by the server..")
                    print("Let's wait for 5 seconds and try again")
                    time.sleep(5)
                    print("Trying again...")
                    continue
        
        info=response.json()
        print(info)


        print(response.status_code)
        #if response.status_code == 201:
        if response.status_code == 200:
            json_data_all = response.json()
            json_data = json_data_all["data"]

            print("Successfully edited the record for the employee: {}".format(json_data))
            return ("Successfully edited the record for the employee: {}".format(json_data))
        else:
            print("Could not edit the employee record. Error: {}".format(info))
            
            return ("Could not edit the employee record. Error: {}".format(info))

    elif request.method == 'GET':
        response = ''
        while response == '':
            try:
                response = requests.get(api_url, headers=header, verify=False)
                break
            except:
                for i in range(3):
                    print("Connection refused by the server..")
                    print("Let's wait for 5 seconds and try again")
                    time.sleep(5)
                    print("Trying again...")
                    continue
        
        #print(response)
        if response.status_code == 200:
            json_data_all = response.json()
            json_data = json_data_all["data"]

            return render_template('homepage.html',json_data=json_data)
        else:
            print("Could not get employee list")
            return "Could not get employee list"
    
    elif request.method == 'DELETE':
        response = ''
        while response == '':
            try:
                response = requests.delete(api_url, headers=header, verify=False)
                break
            except:
                for i in range(3):
                    print("Connection refused by the server..")
                    print("Let's wait for 5 seconds and try again")
                    time.sleep(5)
                    print("Trying again...")
                    continue
        
        #print(response)
        if response.status_code == 200:
            json_data_all = response.json()
            json_data = json_data_all["data"]

            print("Successfully deleted the record: {}".format(json_data))
            return ("Successfully deleted the record: {}".format(json_data))
        else:
            print("Could not delete employee record")
            return "Could not delete employee record"



##### MAIN ##########
header = {"Content-Type": "application/json", "Accept": "application/json"}

if __name__ == '__main__':
    app.run()