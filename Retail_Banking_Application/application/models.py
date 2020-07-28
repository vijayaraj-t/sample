from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Float,Column,String,DateTime,DateTime,CheckConstraint,UniqueConstraint
from application import db

#Model to handle user sessions
class User(UserMixin):
    pass

#Model to store login credentials
    #we assume that currently there is on user
    #IN our case use Email: user@123 Password :123
class Users(db.Model):
    __tablename__='userstore'
    email=Column(String(100),primary_key=True)
    password=Column(String(100))

#Model to handle customer data
class Customers(db.Model):
    __tablename__='customers'
    SSNid=Column(Integer,CheckConstraint('SSNid>99999999 and SSNid<999999999'),primary_key=True)
    customerid=Column(Integer,CheckConstraint('customerid>99999999 and customerid<999999999'),unique=True)
    name=Column(String(30))
    age=Column(Integer,CheckConstraint("age>18 and age<120"))
    address=Column(String(100))
    city=Column(String(20))
    state=Column(String(20))

#Model to handle customer Status
class Customerstatus(db.Model):
    __tablename__='customerstatus'
    SSNid=Column(Integer,CheckConstraint('SSNid>99999999 and SSNid<999999999'),primary_key=True)
    customerid=Column(Integer,CheckConstraint('customerid>99999999 and customerid<999999999'),unique=True)
    status=Column(String)
    message=Column(String)
    lastupdated=Column(DateTime)


#Model to handle customer Accounts
class Accounts(db.Model):
    __tablename__='accounts'
    customerid=Column(Integer,CheckConstraint('customerid>99999999 and customerid<999999999'),unique=True)
    accountid=Column(Integer,CheckConstraint('accountid>99999999 and accountid<999999999'),primary_key=True)
    accounttype=Column(String)
    balance=Column(Integer)
    status=Column(String)
    message=Column(String)
    lastupdated=Column(DateTime)

#Model to handle customer Transactions
class Transactions(db.Model):
    __tablename__='transactions'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer,primary_key=True)
    accountid=Column(Integer())
    customerid=Column(Integer())
    amount=Column(Integer())
    msg=Column(String)
    date=Column(DateTime)
    