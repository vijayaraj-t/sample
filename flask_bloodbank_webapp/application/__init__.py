from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Float,Column,String
import os
app=Flask(__name__)
app.secret_key='NOTHING'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'donordetails.db')

db = SQLAlchemy(app)

class donors(db.Model):
    __tablename__='donors'
    id = Column('bbid',Integer, primary_key = True)
    name=Column(String(100))
    email=Column(String(100))
    password=Column(String(100))
    usertype=Column(String(100))
    contact=Column(String(100))
    address=Column(String(100))
    bloodgroup=Column(String(100))
    dob=Column(String(100))
    age=Column(String(100))
    ioe_name=Column(String(100))
    ioe_contact=Column(String(100))
    ioe_relationship=Column(String(100))

from application import routes
