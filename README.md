# demo-3-tier-app

**Purpose**: I work as a multi-cloud solution architect and as part of the job, often times, I give demos to customers or build specific use cases for them. While doing so I am always looking for an application which is lightweight, is useful (replicates real life use case) and uses 3-tier application architecture (most commonly used architecture).


I searched for such an application but could not find any which suits my requirement. So, I decided **write one myself**. This is the first version of the application. I will provide details of the application here and the required files are also provided here.


Fell free to use, make changes as necessary. Do let me know if you have questions or have modifications in mind.


**Technology Used**: I used the following technologies for the application.

1. Database VM:
  
| Categories       | Components       | 
| -----------------|------------------| 
| Operating System | Ubuntu Server    | 
| Access Method    | REST API         | 
| Programming lang.| Python 3.x       | 
|Apps.| FastAPI, Uvicorn, Gunicorn, Nginx| 


2. Application VM:
  
| Categories       | Components       | 
| -----------------|------------------| 
| Operating System | Alpine Linux    | 
| Access Method    | Web API         | 
| Programming lang.| Python 3.x       | 
|Apps.| Flask, HTML5+CSS+jQuery, Gunicorn|


3. Web VM:
  
| Categories       | Components       | 
| -----------------|------------------| 
| Operating System | Alpine Linux    | 
| Access Method    | Web API         | 
|Apps.| Nginx|


**Reason for choices**: Provided below are the reasons for choosing the technology components.

1. *Database VM*:
  *OS: I chose Alpine linux as the overall OS for the project. Reasoning being Alpine is a small linux with all the flexibilities. The only exception to this is the database VM. For database, I have used Ubuntu Server (22.04) because of the following reasons.
    *MongoDB (6.x) does not have a latest release for Alpine. Current version of Alpine linux is 3.17.x, whereas last available MongoDB version is 5.x on Alpine 3.9.








