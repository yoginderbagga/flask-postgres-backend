# Deploy Flask App on Docker Container using Git Hub Actions on AWS 

### Descriptions

Welcome to this project! In this project, we have build a flask based inventory dashboard for the servers. This web-application keeps track of all the stage, production and development
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

### Key Features

- Containerizatio: Used Docker to containerize the Flask web-application.
- CI CD Pipleline: Used GitHub actions to automate the code deployment.
- Monitoring: Used Grafana, Prometheus, and node-exporter.

### Installation and Configuration Guide

**Envirionment Setup**

This project assume that you already have a AWS Free Tier account and an Ubuntu EC2 installed on it. If not you can do that first and then follow below steps to setup your backend framework using Flask, Gunicorn. 

1. Install python package on Ubuntu EC2.
2. Install Flask package.
3. Install Gunicorn WSGI http server to allow Nginx to communicate with Python.
4. Install Postgresql DB packages for the purpose of data storage and psycopg2 - Python-PostgreSQL Database Adapter
5. Install Nginx package.
6. Install docker package and docker-compose-plugin



**Building the application : Flaskapp**


Once the above packages are installed, you can begin with setting up the [Flaskapp](https://github.com/yoginderbagga/flask-postgres-backend/blob/main/app.py) on your laptop. Proceed with running the app.py application to check if the web-application works or not. As you run the app, go to the browser and verify if the login.html page open for you. Click on the "Register" button to create a new account and then proceed with a fresh login on a new page. 

You may or may not receive an error message depending upon how properly you have followed the instructions to configure this on your machine. Hence I will list down all the challenges, errors I faced in the 
following section but if its working fine for you. Continue following the guide. 

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


Nginx Web-Server Configuration: 



### Challenges During Project





**Directory Structure**

```text
hello/
├── app.py
├── requirements.txt
├── Dockerfile
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
└── static/
```
