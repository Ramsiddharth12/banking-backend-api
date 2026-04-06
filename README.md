# Banking Backend API

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
[![CI/CD Pipeline](https://github.com/Ramsiddharth12/banking-backend-api/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/Ramsiddharth12/banking-backend-api/actions/workflows/docker-ci.yml)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

---

##  Live API
👉 https://banking-backend-gi87.onrender.com

---

## Overview

A **production-style backend system** simulating real-world banking operations, built using Flask and PostgreSQL with secure authentication, transaction management, and a fully automated CI/CD pipeline.

This project demonstrates **end-to-end backend + DevOps workflow**, including containerization, cloud deployment, and conditional infrastructure handling.

---

##  What Makes This Project Strong

-  Secure JWT-based authentication system
-  Real-world banking logic (accounts, transactions, transfers)
-  Fully containerized using Docker
-  Automated CI/CD pipeline using GitHub Actions
-  Multi-environment deployment:
  - **Render (Primary - Always ON)**
  - **AWS EC2 (Secondary - On-demand deployment)**
-  Smart CI/CD design:
  - Handles **EC2 downtime gracefully**
  - Skips deployment if server is unavailable
-  Database migration: SQLite → PostgreSQL

---

##  Architecture

```text
Client (Postman / Frontend)
          |
          v
   Flask API (Docker)
      /           \
     v             v
Render (Always ON)   AWS EC2 (On-Demand)
     \             /
      v           v
      PostgreSQL (Cloud DB)
              ^
              |
        Docker Hub
              ^
              |
      GitHub Actions (CI/CD)
```


---

##  CI/CD Pipeline (GitHub Actions)

### Workflow:

- Triggered on push to `main`
- Builds Docker image using Dockerfile
- Pushes image to Docker Hub
- Checks EC2 availability (port 22)
- Deploys ONLY if EC2 is running

### Key Feature:

>  **Conditional Deployment Logic**
>
> Prevents pipeline failure when EC2 is stopped by skipping the deploy step.
>
> This ensures:
> - Stable CI/CD pipeline
> - Cost-optimized infrastructure usage
> - Real-world DevOps resilience

---

##  Dockerization

- Created a custom Dockerfile
- Built container image for Flask API
- Exposed port `5000`
- Used environment variables for DB configuration
- Pushed image to Docker Hub

 Docker Image:  
https://hub.docker.com/r/ramsiddharth/banking-api

---

##  Deployment Strategy

###  Render (Primary)
- Always live API
- Used for demos and production-like access

###  AWS EC2 (Secondary)
- Docker-based deployment
- Instance started only when needed (cost optimization)
- CI/CD deploys automatically when available

---

##  Authentication & Authorization

- JWT-based authentication
- Role-based access control:
  - **Admin** → manage users, export data
  - **Customer** → perform banking operations

---

##  Features

###  User Management
- Register & Login
- Profile creation
- Role-based access

###  Account Management
- Create account
- View details
- Close account

###  Transactions
- Deposit
- Withdraw
- Transfer funds

###  Data & Tracking
- Transaction history
- Balance checking
- CSV export

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

---

##  Key Concepts Demonstrated

- REST API design
- JWT authentication & authorization
- Role-based access control (RBAC)
- Database relationships & ORM (SQLAlchemy)
- Transaction consistency handling
- Docker containerization
- CI/CD pipeline design
- Conditional deployment logic
- Cloud deployment strategies

---

##  Cost Optimization Strategy

- EC2 instance is **stopped when not in use**
- CI/CD pipeline intelligently skips deployment if EC2 is unavailable
- Prevents unnecessary cloud costs while maintaining pipeline stability

---

##  Testing & Tools

- Postman (API testing)
- DBeaver (database inspection)

---

##  Screenshots

### API Testing
![Postman](assets/postman-tests.png)

### Database
![Database](assets/db-tables.png)

### Render Deployment
![Render](assets/render-deploy.png)

### AWS EC2 Deployment
![AWS](assets/AWS-EC2-deploy.png)

---

##  Challenges Solved

- SQLite → PostgreSQL migration
- Handling JWT across protected routes
- Ensuring transaction consistency
- Debugging CI/CD + SSH failures
- Handling dynamic EC2 public IP changes
- Designing fault-tolerant deployment pipeline

---

##  Future Improvements

- Add Nginx reverse proxy + HTTPS
- Implement logging & monitoring (CloudWatch)
- Add rate limiting & API security
- Introduce auto-scaling infrastructure
- Add Swagger/OpenAPI documentation

---

##  Author/Developer

**Ram Siddharth J**
