# Banking Backend API

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Status](https://img.shields.io/badge/Status-Deployed-success)

**Live API:** https://banking-backend-gi87.onrender.com

A production-ready backend system simulating real-world banking operations, built using Flask and PostgreSQL, with secure authentication and transaction management.

---

## Project Overview

This project implements a complete banking backend system that allows users to:

- Register and login securely using JWT authentication
- Create and manage bank accounts
- Perform transactions like deposit, withdrawal, and transfer
- Track transaction history
- Export transaction data as CSV

The system is deployed on cloud (Render) with a PostgreSQL database.


---

##  Architecture Diagram

Client → Flask API (Docker Container) → PostgreSQL  
                ↓  
           AWS EC2  
                ↓  
           Docker Hub


---

## Objectives

- Build a scalable backend system with real-world banking logic
- Implement secure authentication and authorization
- Ensure data consistency in financial transactions
- Deploy and manage a cloud-based database

---

##  Tech Stack

- **Backend:** Flask (Python)
- **Database:** PostgreSQL (Previously SQLite)
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Deployment:** Render
- **Testing Tools:** Postman, DBeaver

---

##  Authentication & Authorization

- JWT-based login system
- Role-based access:
  - **Admin** → Manage users, export data
  - **Customer** → Perform banking operations

---

##  Features

###  User Management
- Register & Login
- Create profile
- Role-based access (Admin / Customer)

###  Account Management
- Create bank account
- View account details
- Close account

###  Transactions
- Deposit money
- Withdraw money
- Transfer funds between accounts

###  Data & Tracking
- Transaction history per user
- Balance checking
- CSV export for transactions

---

##  API Endpoints

### Authentication
- `POST /register`
- `POST /login`

### Account & Profile
- `POST /createprofile`
- `POST /createaccount`
- `PUT /Changedetails/<accno_last4>`
- `DELETE /AccountClose/<accno_last4>`

### Transactions
- `POST /deposit`
- `POST /withdraw`
- `POST /transfer`

### Data Retrieval
- `GET /your/accounts&details`
- `GET /balance`
- `GET /your/transactions`

### Admin
- `GET /all/customersdetails`
- `GET /all/transactions`
- `GET /admin/export/<value>`
- `POST /addcustomer`
- `POST /admin/register`

### Export
- `GET /transaction/export/<accno_last4>`

---

##  Key Concepts Implemented

- REST API design principles
- JWT authentication & token handling
- Role-based authorization
- Database relationships (Users, Accounts, Transactions)
- Transaction consistency handling
- Cloud deployment (Render + PostgreSQL)

---

##  Deployment

- Backend deployed on Render
- PostgreSQL database hosted on Render
- External DB access via DBeaver


## Docker & AWS Deployment

The application was containerized using Docker and deployed on an AWS EC2 instance.

### Docker

- Created a Dockerfile to containerize the Flask application  
- Built Docker image locally  
- Pushed image to Docker Hub  

Docker Hub Image:  
https://hub.docker.com/r/ramsiddharth/banking-api

### AWS Deployment

- Launched EC2 instance (Ubuntu)  
- Installed Docker on EC2  
- Pulled Docker image from Docker Hub  
- Ran container and exposed port 5000  
- Accessed application via EC2 public IP  

Example:

docker pull ramsiddharth/banking-api:latest  
docker run -d -p 5000:5000 ramsiddharth/banking-api

---

##  Screenshots

###  - API Testing (Postman)
![Postman](assets/postman-tests.png)

###  - Database View (DBeaver)
![Database](assets/db-tables.png)

###  - Deployment (Render)
![Render](assets/render-deploy.png)

### - AWS (Deployment)
![Render](assets/AWS-EC2-deploy.png)


---


##  Challenges Faced

- Handling database migration (SQLite → PostgreSQL)
- Managing JWT authentication across endpoints
- Ensuring transaction consistency
- Debugging cloud deployment issues

---

##  Future Improvements

- Add rate limiting (security)
- Implement logging & monitoring
- Add Swagger API documentation
- Improve error handling
- Implement CI/CD pipeline for automated deployment
---

##  Author/Developer

**Ram Siddharth J**
