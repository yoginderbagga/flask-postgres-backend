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
4. Install Postgresql DB packages for the purpose of data storage.
5. Install Nginx package.


**Building the application : Flaskapp**

Once the above packages are installed, you can being with setting up the [Flaskapp](https://github.com/yoginderbagga/flask-postgres-backend/blob/main/app.py) on your laptop. 

### Challenges During Project
