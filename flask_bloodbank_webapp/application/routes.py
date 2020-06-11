from flask import Flask,render_template,redirect,url_for,request,flash,session
import sqlite3,os
from application import app,db,donors
from datetime import timedelta

app.permanent_session_lifetime=timedelta(minutes=5)

login_status=0
@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    f=0
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        validate=donors.query.filter_by(email=email,password=password).first()
        print(validate)
        if validate:
            flash("login sucessful")
            f=1
            session.permanent=True
            session['user']=123
            session['usertype']=validate.usertype
            return redirect(url_for('index'))    
        if f==0: 
            flash("Incorrect password/user doesnt exist")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        db.create_all()
        donor=donors(name=request.form.get('name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        usertype=request.form.get('usertype'),
        contact=request.form.get('contact'),
        address=request.form.get('address'),
        bloodgroup=request.form.get('bloodgrp'),
        dob=request.form.get('dob'),
        age=request.form.get('age'),
        ioe_name=request.form.get('ioe_name'),
        ioe_contact=request.form.get('ioe_contact'),
        ioe_relationship=request.form.get('ioe_relationship'))
        db.session.add(donor)
        db.session.commit()
        flash("Registration Sucessful")
        return redirect(url_for('index'))
    return render_template('signup.html')
    
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST' and 'bloodgrp' in request.form:
        bloodgrp=request.form.get('bloodgrp')
        matches=[]
        matches=donors.query.filter_by(bloodgroup=bloodgrp).all()
        if len(matches)>0:
            return render_template('search.html',matches=matches)
        flash("NO Matches Found")
    if request.method=='POST' and 'bbid' in request.form and session['usertype']=='admin':
        bbid=request.form.get('bbid')
        matches=[]
        matches=donors.query.filter_by(id=bbid).all()
        if len(matches)>0:
            return render_template('search.html',matches=matches)
        flash("NO Matches Found")
    return render_template('search.html',login_status=login_status)
    