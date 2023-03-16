**Purpose:**

I work as a multi-cloud solution architect and as part of the job, often times, I give demos to customers or build specific use cases for them. While doing so I am always looking for an application which is lightweight, is useful (replicates real life use case) and uses 3-tier application architecture (most commonly used architecture).

I searched for such an application but could not find any, which, suits my requirement. So, I decided **write one myself**. This is the first version of the application. I will provide details of the application here and the required files are also provided here.

Feel free to use, make changes as necessary. Do let me know if you have questions or have modifications in mind.

**Application Structure:**

This is going to be a 3-tier application. With database as backend, app server as mid tier and web server as front tier.

**Technology Used:**

I used the following technologies for the application.

1. **Database VM:**

|**Categories**|**Components**|
| :-: | :-: |
|Operating System|Ubuntu Server|
|Access Method|REST API|
|Programming lang.|Python 3.x|
|Apps.|FastAPI, Uvicorn, Gunicorn, Nginx|
2. **Application VM:**

|**Categories**|**Components**|
| :-: | :-: |
|Operating System|Alpine Linux|
|Access Method|Web API|
|Programming lang.|Python 3.x|
|Apps.|Flask, HTML5+CSS+jQuery, Gunicorn|
3. **Web VM:**

|**Categories**|**Components**|
| :-: | :-: |
|Operating System|Alpine Linux|
|Access Method|Web API|
|Apps.|Nginx|
**Reasoning:**

Provided below are the reasons for choosing the technology components.

- **Platform:**

|Tier|OS|
| :- | :- |
|Database|Ubuntu Server 22.04 (lts)|
|Application|Alpine Linux 3.17.1|
|Web|Alpine Linux 3.17.1|
**Reasoning**: 

Overall I chose Alpine linux for all other component except database VM.

- MongoDB Support: Latest version of MongoDB (6.x) does not have a release for current Alpine version. Current version of Alpine linux is 3.17.x, whereas last available MongoDB version is 5.x on Alpine 3.9. Using older versions will force me to use older versions for all the other component. This is undesirable and increases complexity. Using Ubuntu as OS increased the overall footprint but gain outweighs the disadvantage here.
- Size of the VM: Alpine linux is much smaller in size in comparison with Ubuntu VM. This suits perfectly the app and the web vm's but for database vm we need more libraries. With all the libraries size becomes considerably larger for Alpine Linux. Hence Ubuntu was chosen as DB VM.

**How to:**

Provided below are the details of the configuration. Since here I am providing all the program files, servers need to be configured as per detail below. I also plan to create a OVA file with everything pre-configured. That would not require the below configurations.

**Database VM:**

- I have included a sample database with 500 entries. The sample data was generated using [Mockaroo. ](https://www.mockaroo.com/) 
  - Database Name: employees\_DB
  - Collection Name: employees
  - Structure: 
    - "\_id": ObjectId
    - "emp\_id": int
    - "first\_name": str
    - "last\_name": str
    - "email": str
    - "ph\_no": str
    - "home\_addr": str
    - "st\_addr": str
    - "gender": str
    - "job\_type": str
- Install MongoDB on the VM using the [method detailed](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) in the website.
- After installing MongoDB, create a folder where you want to keep all the required files. For example, employee\_db.
- Download all the files under DB VM repository and copy it over to employee\_db folder. The files under the DB VM repository are listed below: 
  - MOCK\_DATA.json - contains the mock data
  - app.py - Python file containing the application
  - employee\_database.py - Has the details on how to access the database and all the required functions to handle database operations.
  - employee\_models.py - This file defines the models for handling the data from the database. This aligns with the database collection schema.
  - employee\_routes.py - This file has all the routes for the application.
  - requirements.txt - Has all the components needed to be installed for the application to be working. 
    - fastapi - component which creates the REST API endpoints and Swagger UI
    - uvicorn - Uvicorn is an ASGI web server implementation for Python
    - pydantic[email] - Data validation and settings management using Python type annotations
    - motor - Asynchronous python driver for MongoDB
    - gunicorn - The Gunicorn "Green Unicorn" is a Python Web Server Gateway Interface HTTP server
- Supported CRUD operations: 

GET /employee: to list all employees
GET /employee/<emp\_id>: to get an employee by employee ID
POST /employee: to create a new employee record
PUT /employee/<emp\_id>: to update an employee record by employee ID
DELETE /employee/<emp\_id>: to delete an employee record by employee ID

- Running NGINX+ GUNICORN + UVICORN in DB VM. Note, the following configurations assume you have an existing user by name "user" present in the Ubuntu VM. Otherwise, replace it with your user id.

sudo apt install supervisor nginx -y
sudo systemctl enable supervisor
sudo systemctl start supervisor
nano /home/user/employee\_db/gunicorn\_start

#!/bin/bash

NAME=fastapi-mongodb-app
DIR=/home/user/employee\_db
USER=user # This is the user id with which you are installing everything
GROUP=user
WORKERS=3
WORKER\_CLASS=uvicorn.workers.UvicornWorker
BIND=unix:$DIR/run/gunicorn.sock
LOG\_LEVEL=error

cd $DIR

exec gunicorn app:app \
`  `--name $NAME \
`  `--workers $WORKERS \
`  `--worker-class $WORKER\_CLASS \
`  `--user=$USER \
`  `--group=$GROUP \
`  `--bind=$BIND \
`  `--log-level=$LOG\_LEVEL \
`  `--log-file=-

chmod u+x gunicorn\_start
cd /home/user/employee\_db
mkdir run
mkdir logs

sudo nano /etc/supervisor/conf.d/fastapi-mongodb-app.conf

[program:fastapi-mongodb-app]

command=/home/user/employee\_db/gunicorn\_start
user=user
autostart=true
autorestart=true
redirect\_stderr=true
stdout\_logfile=/home/user/mongodb/logs/gunicorn-error.log


sudo supervisorctl reread
sudo supervisorctl update

To update code:

sudo supervisorctl restart fastapi-app

Configure NGINIX:

**sudo nano** /etc/nginx/sites-available/fastapi-mongodb-app

upstream app\_server {
`    `server unix:/home/user/employee\_db/run/gunicorn.sock fail\_timeout=0;
}

server {
`    `listen 80;
`    `# add here the ip address of your server
`    `# or a domain pointing to that ip (like example.com or [www.example.com](http://www.example.com))
`    `server\_name <Server IP/FQDN>;

`    `keepalive\_timeout 5;
`    `client\_max\_body\_size 4G;

`    `access\_log /home/user/employee\_db/logs/nginx-access.log;
`    `error\_log /home/user/employee\_db/logs/nginx-error.log;

`    `location / {

`        `proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;
`        `proxy\_set\_header Host $http\_host;
`        `proxy\_redirect off;

`        `if (!-f $request\_filename) {
`            `proxy\_pass <http://app_server>;
`            `break;
`        `}
}
}


sudo ln -s /etc/nginx/sites-available/fastapi-mongodb-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

**Note**: Change the user in /etc/nginx/nginx.conf from www-data to "user".

**Application VM:**

- Deploy an Alpine linux VM.
- Install the dependencies: 
  - Install flask:

apk add python3  --no-cache
python3 -m ensurepip  
pip3 install --upgrade pip
pip3 install flask  

  - Install gunicorn

apk add py3-gunicorn  --no-cache

- Create a folder /root/employee\_app 
- Copy all the files including the structure inside /root/employee\_app folder
- Run gunicorn server as service in Alpine:

**vi /etc/local.d/gunicorn.start**

#!/bin/sh
cd /root/employee\_app

nohup /usr/bin/gunicorn --bind 0.0.0.0:8080 app:app  &

**chmod 755 /etc/local.d/gunicorn.start**

- Reboot the server. Now the application is available on http://<app-vm-ip>:8080

**Web VM:**

- Deploy an Alpine linux VM.
- Install Nginix:

apk add nginx  --no-cache
rc-update add nginx default

- Configure Nginix as reverse proxy:

**vi  /etc/nginx/http.d/default.conf**

\# This is a default site configuration which will simply return 404, preventing
\# chance access to any other virtualhost.

server {
`        `listen 80 default\_server;
`        `listen [::]:80 default\_server;
`        `server\_name <web-server-ip or fqdn>;
`        `# Everything is a 404
`        `location / {
`                `proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;
`                `proxy\_set\_header Host $http\_host;
`                `proxy\_redirect off;

`                `if (!-f $request\_filename) {
`                        `proxy\_pass http://<app-server-ip or fqdn>:8080;
`                        `break;
`                `}
`                `#return 404;
`        `}

`        `# You may need this to prevent return 404 recursion.
`        `location = /404.html {
`                `internal;
`        `}
}

Now the application can be accessed by going to http://<web-server-ip or fqdn> Swagger UI is available for DB at http://<db-vm-ip or fqdn>/docs or http://<db-vm-ip or fqdn>/redoc 

**Sample Screenshots**

Provided below are few sample screenshots.

**Swagger UI and Redocs**

Swagger UI Redoc UI 

**Application UI**

The application UI is self explanatory. Explore the options and hope you will like it.









