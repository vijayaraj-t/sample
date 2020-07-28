from flask import Flask
from flask_login import login_manager,login_required,login_user,logout_user,LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
import os

#app initialized
app=Flask(__name__)
app.secret_key='NOTHING'

#configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bankdetails.db')
db = SQLAlchemy(app)

#create database
if __name__=='__main__':
    db.create_all()

login_manager=LoginManager()
login_manager.init_app(app)

from application.models import User,Users

#user loader and session loader for session management 
@login_manager.user_loader
def user_loader(email):
    validate=Users.query.filter_by(email=email).first()
    if not validate:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    validate=Users.query.filter_by(email=email).first()
    if not validate:
        return
    user = User()
    user.id = email
    user.is_authenticated=request.form['password']==Users.query.get('password')
    return user
    
from application import routes
