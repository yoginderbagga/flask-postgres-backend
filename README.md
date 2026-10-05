# Deploy Flask App on Docker Container using Git Hub Actions on AWS 

### Descriptions

Welcome to this project! Here, we have build a flask based inventory dashboard for the servers. This web-application keeps track of all the stage, production and development
servers currently available in the database. With this app, users can quickly check the status of total servers, delete, and edit the records. Since we have used docker to 
containerized it, you can easily setup the app on your Mac, Linux and Windows machine. This is completely hosted on AWS Coud to keep the cost as minimum as possible, and we have
also added monitoring functionality using the Grafana, prometheus tool. Using that you can check the performance of your EC2 Instance with stats like : CPU Basic, Memory Basic,
Network Traffic Basic, Disk Space Basic and much more. 


### Technical Requirements

- Python 3.14.4
- Nginx
- Flask
- Gunicorn
- AWS EC2, VPC Security Group
- Docker
- GitHub Actions
- Postgre SQL
- pgAdmin     [ Not using this : Flaskapp directly connecting with Postgresql DB on my EC2 instance docker ]
- MS Visual Code
- Grafana
- Prometheus
- Node Exporter
- SonarQube

**Directory Structure**

```text
hello/
├── app.py
├── requirements.txt
├── Dockerfile
├── myenv
├── monitoring
├── sonar-project.properties
├── docker-compose.yml
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── monitoring/
│   └── prometheus.yml
├── .github/
│   └── workflows/
│       └── deploy.yml
| 
└── static/
```

### Key Features

- Containerizatio: Used Docker to containerize the Flask web-application.
- CI CD Pipleline: Used GitHub actions to automate the code deployment.
- Monitoring: Used Grafana, Prometheus, and node-exporter.

### Installation and Configuration Guide

**Envirionment Setup**

This project assume that you already have a AWS Free Tier account and an Ubuntu EC2 installed on it. If not you can do that first and then follow below steps to setup your backend framework using Flask, Gunicorn. Everything will be accessed via the EC2 host URL only with the respective port of the application. 

1. Install python package on Ubuntu EC2.
2. Install Flask package.
3. Install Gunicorn WSGI http server to allow Nginx to communicate with Python.
4. Install Postgresql DB packages for the purpose of data storage and psycopg2 - Python-PostgreSQL Database Adapter
5. Install Nginx package.
6. Install docker package and docker-compose-plugin



**Building the application : Flaskapp (Flask, Gunicorn, Nginx)**


Once the above packages are installed, you can begin with setting up the [Flaskapp](https://github.com/yoginderbagga/flask-postgres-backend/blob/main/app.py) on your laptop. Proceed with running the app.py application to check if the web-application works or not. As you run the app, go to the browser and verify if the login.html page open for you. Click on the "Register" button to create a new account and then proceed with a fresh login on a new page. 

You may or may not receive an error message depending upon how properly you have followed the instructions to configure this on your machine. Hence I will list down all the challenges, errors I faced in the 
following section but if its working fine for you. Continue following the guide. 

- Flask: A python framework for building lightweight, web-applications and APIs. It basically handles the backend logic, process the browser requests, track user session and display dynamic HTML pages. 
- Nginx Reverse Proxy: Intruders are always there to crash a live web-application at anytime. Hence its always critical to protect the web-application from hackers. But doing so becomes difficult when there are thousands of users visiting the website at the same time. Nginx Reverse Proxy is middle layer which sits between the user like "Rajkumar" ( visiting the site) and the actual web-server where the content is stored (AWS EC2 Instance). Instead of sending all the user requests to the backend logic directly -- all requests go through the reverse proxy, which then makes a decision which server should handle the "Rajkumar", "John" or "Lima" requests. Reverse proxy also plays crucial role in load balancing by equally distributing the incoming traffic to prevent overload. 
- Gunicorn: A traditional Nginx web-server can not directly execute the python code, because Nginx primarily use to server the HTML, CSS, images like websites. This problem gets solved by Gunicorn which bridges this gap by converting the incoming HTTP requests from the web-server into a format the Python app can understand and execute the code and then prepare a response for the user. 

**Monitoring the application : Prometheus + Grafana + Node Exporter**

- Node Exporter: A simple lightweight application which collects Unix based OS metrics and hardware info and then transfer them to relevant application for the monitoring purpose. Metrics include: ``CPU load`` ``memory consumption``, ``disk usage``, ``network traffic`` and much more. Remember that "Node Exporter" never stored any data which it collects in any database, any storage layer or memory cache. Basically it fetches the live data for Prometheus to monitor and analyze. 
- Prometheus: An open-source monitoring tool which gather the data from Node Exporter (or other tool), and store it as a time series data. It actively pulls live data by sending the HTTP request to targe server at regular intervals. 
- Grafana: It is prominent data visualization tool used with Prometheus to build the dashboard of your metrics stats. 


## Phase 1 — Initial EC2 Setup
#### Step a) — Go to your AWS Account and Launch EC2 Instance ( t3.micro ) and allow the inbound security groups including :
- 8000 : For flask web-app connectivity
- 3000 : For Grafana monitoring tool
- 9090 : For Prometheus 
- 9100 : For Node exporter.

#### Step b) — SSH to the EC2 instance using the public IP address as you will be doing all work on AWS Cloud instance. 

```
ssh -i your-key.pem ubuntu@EC2-PUBLIC-IP
```

#### Step c) — Update the Ubuntu packages to ensure Ubuntu OS have relevant updates. 

```
sudo apt update && sudo apt upgrade -y
```

## Phase 2 — Setting up the Flaskapp web-application ( First build without the dockerization )
#### Step a) — Install the Python packages, dependencies and GIT package. 

```
sudo apt install python3-pip python3-venv nginx git -y
```
#### Step b) — Clone project repository on your EC2 instance ~/hello folder

```
git clone git@github.com:yoginderbagga/flask-postgres-backend.git
cd hello
```

#### Step c) —  Setup a virtual environment for your python code to keep it seperate with rest of your system applications. 
```
python3 -m venv venv
source venv/bin/activate
```
#### Step d) —  Installing Flask Requirements

```
pip install -r requirements.txt
```
#### Step e) —  Run Flask Application

```
python3 app.py
```

## Phase 3 —  Nginx Web-Server Configuration and Gunicorn setup

#### Step a) — Install Gunicorn WSGI HTTP Server for allowing the python object to communicate with the nginx server. 

```
pip install gunicorn
```
#### Step b) —  Start the Gunicorn

```
gunicorn -b 0.0.0.0:8000 app:app
```
#### Step c)  — Configuring the Nginx revere proxy server. 
Create a configuration file for flaskapp in the Nginx configuration directory : "/etc/nginx/sites-available/flaskapp"

```
server {
    listen 80;

    server_name EC2_PUBLIC_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Step d)  —  Enable Nginx Site

```
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
```
#### Step e)  —  Test Nginx Configuration

```
sudo nginx -t
```
#### Step f)  —  Restart Nginx serverice 

```
sudo systemctl restart nginx
```

## Phase 4 —   Implementing systemd service unit to make the web-app start right after the reboot ( earlier deployment model ) 

Create a service unit file 

```
sudo nano /etc/systemd/system/flaskapp.service
```

```
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hello
Environment="PATH=/home/ubuntu/hello/venv/bin"
ExecStart=/home/ubuntu/hello/venv/bin/gunicorn -b 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
Enabled the systemd unit service for flaskapp
```
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

## Phase 5 — Migrate to dockerize architecture for the flaskapp.


### What were the challenges during the project setup and troubleshooting steps?

[Updated : 27th Sep, 2026]

- Error during migrating the application to Docker Compose: Below error received, when registering the user details on login page. In ``app.py`` go to the custom database connection function, and found that hostname was  ``host="localhost"`` which works only for your localhost environment. However, if use ``db`` then it does works, because each time you restart the EC2 instance or change the IP address then docker don't have to worry about the IP address. ( While localhost will only point to that specific container, and db is the service name in the docker compose file)
- [ Update : 4th Oct] Removed the ports 5432 entirely along with the containers name from the docker-compose file. Now I verified even after the restart of the machine or next day, it doesn't give the previous DNS error message anymore. 
- Error during data insertion, since there was no database, table created, you need to verify this as well if they still exists or not. (**Later** create a proper backup so each time you don't have to create the table again and again) 



```
 File "/app/app.py", line 31, in register
    conn = get_db_connection()
           ^^^^^^^^^^^^^^^^^^^
  File "/app/app.py", line 9, in get_db_connection
    return psycopg2.connect(
           ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
	Is the server running on that host and accepting TCP/IP connections?
connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
	Is the server running on that host and accepting TCP/IP connections?

### Date: 29th Sep, 2026

- After submitting the user info, it gave error message for the internal server. Had to rebuild the containers with docker compose. ( Possibly due to docker compose networking issue )
- Error during continuous integration, as the one of the action in pipeline didn't run. SSH issue was there since EC2 IP address was changed, after updating the latest public IP in GitHub Actions Secret it worked. 

```

### Project Screenshots - Final Output

#### Application Output:


<img width="1897" height="1067" alt="image" src="https://github.com/user-attachments/assets/a2ae379a-60c3-44c0-8348-283909bbdb13" />

<img width="1905" height="1072" alt="image" src="https://github.com/user-attachments/assets/cc182c9a-9e96-4ec0-a3bd-2d803b8001f8" />

<img width="1902" height="560" alt="image" src="https://github.com/user-attachments/assets/241921f5-858e-47d2-86c0-c7f48334f720" />

#### Monitoring Stack: 


<img width="1900" height="1070" alt="image" src="https://github.com/user-attachments/assets/4918f6d9-dfda-4306-9e0f-af3b901f725f" />

<img width="1902" height="790" alt="image" src="https://github.com/user-attachments/assets/affd665e-6e8f-4444-bd54-e5985c21cdab" />



### Continuous Integration - Pipeline Output

To test the pipeline, go to the login.html file make a change at the text login with "Test Login" and commit the changes. Verified at "Actions" tab and pipeline ran fine, below is the result. 

<img width="1900" height="1032" alt="image" src="https://github.com/user-attachments/assets/5ea04fe6-83eb-4c9b-92ec-45a0186c34de" />

<img width="1892" height="1077" alt="image" src="https://github.com/user-attachments/assets/6743c435-6d94-49dd-9793-1a2bffc6b0e0" />


Output # 2 

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/798d5274-bdee-4d4a-97db-67420cd93962" />

### Continuous Integration - Added SonarQube"

- Added SonarQube for Static Code Analysis, catch bugs, security vulnerability scanning before the code reach the production.
- Added Dependency Caching so that cache packages can be reused instead of re-downloading them each time in fresh runner.

