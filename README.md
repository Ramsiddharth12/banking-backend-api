\# **Banking Backend API**



**A Flask-based backend system simulating real-world banking operations.**



\## **Features**

\- JWT Authentication (Login/Register)

\- Role-based access (Admin / Customer)

\- Account creation \& management

\- Deposit / Withdraw / Transfer

\- Transaction history tracking

\- CSV export (Admin \& Customer)



\## **Tech Stack**

\- Python

\- Flask

\- SQLAlchemy

\- SQLite (can be upgraded to PostgreSQL)

\- JWT Authentication



\## **API Endpoints**

\- /register

\- /login

\- /createaccount

\- /createprofile

\- /addcustomer

\- /AccountClose/<accno\_last4>

\- /Changedetails/<accno\_last4>

\- /customerdetail

\- /allcustomersdetails

\- /balance

\- /SingleCustomerTransactions

\- /transaction/export/<accno\_last4>

\- /admin/export/<value>

\- /deposit

\- /withdraw

\- /transfer

\- /transactions





\##  **Future Improvements**

\- Deploy on cloud (Render / AWS)

\- Switch to PostgreSQL

\- Add rate limiting

\- Add logging



\## **Author**

Ram Siddharth J

