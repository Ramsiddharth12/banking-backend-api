from dbapp import db
from sqlalchemy import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
     
    __tablename__ = "customers"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    age=db.Column(db.Integer, nullable=False)
    phone=db.Column(db.String(20), unique=True, nullable=False)

    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True)


class Transaction(db.Model):

    __tablename__ = "transactions"
    id=db.Column(db.Integer, primary_key=True)
    action=db.Column(db.String(30), nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    balance_before= db.Column(db.Integer, nullable=False)
    balance_after= db.Column(db.Integer, nullable=False)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)

    account_id=db.Column(db.Integer, db.ForeignKey("accounts.id"),nullable=False)


class User(db.Model):

    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(Enum("customer","admin", name="role_enum"), nullable=False)

    customer_id=db.Column(db.Integer, db.ForeignKey("customers.id"), unique=True, nullable=True)

    def set_password(self,password):
         self.password_hash=generate_password_hash(password)

    def check_password(self,password):
         return check_password_hash(self.password_hash,password)


class Account(db.Model):
        
        __tablename__="accounts"
        id=db.Column(db.Integer, primary_key=True)
        account_number=db.Column(db.String(20), unique=True, nullable=False)
        account_type=db.Column(Enum("savings","current", name="account_type_enum"),nullable=False)
        balance=db.Column(db.Integer, nullable=False)
        
        customer_id=db.Column(db.Integer, db.ForeignKey("customers.id"),nullable=False)        
                
        transactions=db.relationship("Transaction",backref="account",cascade="all, delete-orphan",lazy=True) 