from    application         import db,app
from    flask               import render_template,redirect,url_for,request,session,flash
from    sqlalchemy.orm      import Session
from    sqlalchemy          import and_,desc
import  datetime
from    flask_login         import login_manager,login_required,login_user,logout_user,LoginManager,UserMixin
from    application.models  import User,Customers,Customerstatus,Accounts,Users,Transactions


@app.route('/')
@app.route('/home')  #route for home page
def home():
    db.create_all()
    return render_template('home.html')

@app.route('/login',methods=["GET","POST"])     #route for login page
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        validate=Users.query.filter_by(email=email,password=password).first() 
        if validate:
            user = User()   #creating a session for current user
            user.id = email
            login_user(user)
            flash("Login sucessful")
            return redirect(url_for('home'))
        else:
            flash("Incorrect password / Invalid User")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')     #route for logout page
@login_required             #Restricts page from unknown users
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/addcustomer',methods=['GET','POST'])     #route for addcustomer page
@login_required             #Restricts page from unknown users
def addcustomer():
    if request.method=='POST':
        SSNid=request.form.get('SSNid')
        customerid=request.form.get('customerid')
        name=request.form.get('name')
        age=request.form.get('age')
        addr1=request.form.get('addr1')
        addr2=request.form.get('addr2')
        address=addr1+" "+addr2
        city=request.form.get('city')
        state=request.form.get('state')
        status='Active'
        message='Account Created'
        lastupdated=datetime.datetime.now()
        msg=addnew(SSNid,customerid,name,age,address,city,state,status,message,lastupdated)
        if not msg:   
            flash('Constrains failed')                  #Error/Response messages are flashed to screen
            return redirect(url_for('addcustomer'))
        else:
            flash("Customer created sucessfully")
            return redirect(url_for('home'))
    else:
        return(render_template('addcustomer.html'))

@app.route('/editcustomer',methods=['GET','POST'])     #route for Edit customer page
@login_required
def editcustomer():
    if not 'id' in request.args:
        return redirect(url_for('editvalidate'))
    if 'id' in request.args and request.method != 'POST':    
        customerid=request.args.get('id',None)
        customerid=int(customerid)
        customer=Customers.query.filter_by(customerid=customerid).first()
        return render_template('editcustomer.html',customer=customer)
    if request.method =='POST':
        name=request.form.get('name')
        age=request.form.get('age')
        address=request.form.get('address')
        city=request.form.get('city')
        state=request.form.get('state')
        customerid=request.form.get('customerid')
        message='Update Sucessful'
        lastupdated=datetime.datetime.now()         #update last updated using  datetime function
        try:
            a_user = Customers.query.filter_by(customerid=customerid).first()
            a_user.name = name
            a_user.age = age
            a_user.city = city
            a_user.state = state
            a_user.address = address
            b_user = Customerstatus.query.filter_by(customerid=customerid).first()
            b_user.message = message
            b_user.lastupdated =lastupdated
            db.session.commit()
            flash("Customer Updated Sucessfully")
            return redirect(url_for('home'))
        except:
            flash('Error Updating')
            return redirect(url_for('editcustomer'))

@app.route('/editvalidate',methods=['GET','POST'])     #route for validate user page
@login_required
def editvalidate():
    if request.method=='POST' and 'SSNid' in request.form  :
        SSNid=request.form.get('SSNid')
        validate=Customers.query.filter_by(SSNid=SSNid).first()
        if validate:
            id=validate.customerid
            return redirect(url_for('editcustomer',id=id))
        else:
            flash("Invalid SSNid !")
            return redirect(url_for('editvalidate'))
    if request.method=='POST' and 'customerid' in request.form :
        customerid=request.form.get('customerid')
        validate=Customers.query.filter_by(customerid=customerid).first()
        if validate:
            id=validate.customerid
            return redirect(url_for('editcustomer',id=id))
        else:
            flash("Invalid CustomerId !")
            return redirect(url_for('editvalidate'))

    if request.method !='POST':
        return render_template('editvalidate.html')

@app.route('/deletevalidate',methods=['GET','POST'])     #route for validate user before delete
@login_required
def deletevalidate():
    if request.method=='POST' and 'SSNid' in request.form  :
        SSNid=request.form.get('SSNid')
        validate=Customers.query.filter_by(SSNid=SSNid).first()
        if validate:
            id=validate.customerid
            return redirect(url_for('deletecustomer',id=id))
        else:
            flash("Invalid SSNid !")
            return redirect(url_for('deletevalidate'))
    if request.method=='POST' and 'customerid' in request.form :
        customerid=request.form.get('customerid')
        validate=Customers.query.filter_by(customerid=customerid).first()
        if validate:
            id=validate.customerid
            return redirect(url_for('deletecustomer',id=id))
        else:
            flash("Invalid CustomerId !")
            return redirect(url_for('deletevalidate'))

    if request.method !='POST':
        return render_template('deletevalidate.html')

@app.route('/deletecustomer',methods=['GET','POST'])     #route for delete customer page
@login_required
def deletecustomer():
    if not 'id' in request.args:
        return redirect(url_for('deletevalidate'))
    if 'id' in request.args and request.method != 'POST':     
        customerid=request.args.get('id',None)
        customerid=int(customerid)
        customer=Customers.query.filter_by(customerid=customerid).first()
        return render_template('deletecustomer.html',customer=customer)
    if request.method=='POST':
        customerid=request.form.get('customerid')
        try:
            user2=Customerstatus.query.filter_by(customerid=customerid).first()
            user2.message='Deletion Successful'
            user2.lastupdated=datetime.datetime.now()
            user2.status='Deactivated'
            db.session.commit()
            flash("Customer Deletion Sucessful")
            return redirect(url_for('home'))
        except:
            flash("Something Wrong in Deletion")
            return redirect(url_for('deletecustomer'))


@app.route('/customerstatus')     #route for customer status page
@login_required
def customerstatus():
    customers=Customerstatus.query.all()
    return render_template('customerstatus.html',customers=customers)

@app.route('/viewcustomer',methods=['GET','POST'])     #route for view customer page
@login_required
def viewcustomer():
    if request.method=='POST':
        customerid=request.form.get('customerid')
        customer=Customers.query.filter_by(customerid=customerid).first()
        if customer:
            return render_template('viewcustomer.html',customer=customer)
    return None


@app.route('/createaccount',methods=['GET','POST'])     #route for create account page
@login_required
def createaccount():
    if request.method=='POST':
        customerid=request.form.get('customerid')
        accountid=request.form.get('accountid')
        accounttype=request.form.get('accounttype')
        depositamount=request.form.get('depositamount')
        accountstatus='Active'
        message='Account created sucessfully'
        lastupdated=datetime.datetime.now()
        customer=Customerstatus.query.filter_by(customerid=customerid).first()
        if customer:
            if customer.status=='Active':
                account=Accounts(customerid=customerid,accountid=accountid,accounttype=accounttype,
                                balance=depositamount,status=accountstatus,message=message,
                                lastupdated=lastupdated)        
                transaction=Transactions(customerid=customer.customerid,accountid=accountid,amount=depositamount,msg="Debit",date=lastupdated)
                try:
                    db.session.add(account)
                    db.session.add(transaction)
                    db.session.commit()
                    flash('Account Added Sucessfully')
                    return redirect(url_for('home'))
                except:
                    flash('Constrains Failed')
                    return redirect(url_for('home'))
            else:
                flash('Customer Deactivated')
                return redirect(url_for('Home'))
        else:
            flash('Invalid Customerid / Account Inactive')
            return redirect(url_for('createaccount'))
    else:
        return render_template('createaccount.html')

@app.route('/deleteaccount',methods=['GET','POST'])     #route for delete account page
@login_required
def deleteaccount():
    if request.method=='POST':
        accountid=request.form.get('accountid')
        accounttype=request.form.get('accounttype')    
        account=Accounts.query.filter_by(accountid=accountid,accounttype=accounttype).first()
        if account:
            account.message='Account Deleted'
            account.lastupdated=datetime.datetime.now()
            account.status='Deactivated'
            db.session.commit()
            flash('Account deleted Sucessfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid Customerid / account type')
            return redirect(url_for('deleteaccount'))
    else:
        return render_template('deleteaccount.html')

@app.route('/accountstatus')     #route for account  status page
@login_required
def accountstatus():
    accounts=Accounts.query.all()
    return render_template('accountstatus.html',accounts=accounts)

@app.route('/searchcustomer',methods=['GET','POST'])         #route for Search customer page
@login_required
def searchcustomer():
    if request.method=='POST' and 'cid' in request.form:
        customerid=request.form.get('cid')
        customer=Accounts.query.filter_by(customerid=customerid).first()
        if customer:
            return render_template('searchresult.html',customer=customer)
        else:
            flash('Invalid customer id')
            redirect(url_for('searchcustomer'))
    if request.method=='POST' and 'aid' in request.form:
        accountid=request.form.get('aid')
        customer=Accounts.query.filter_by(accountid=accountid).first()
        if customer:
            return render_template('searchresult.html',customer=customer)
        else:
            flash('Invalid Account id')
            redirect(url_for('searchcustomer'))
    return render_template('searchcustomer.html')



def addnew(SSNid,customerid,name,age,address,city,state,status,message,lastupdated):
    customer=Customers(SSNid=SSNid,customerid=customerid,name=name,age=age,
                            address=address,city=city,state=state)
    customerstatus=Customerstatus(SSNid=SSNid,customerid=customerid,status=status,
                                    message=message,lastupdated=lastupdated)
    try:
        db.session.add(customer)
        db.session.add(customerstatus)
        db.session.commit()
        return True
    except:
        return False



@app.route('/deposit',methods=['GET','POST'])     #route for deposit money page
@login_required
def deposit():
    if request.method == 'POST':
        accountid = request.form.get('accountid')
        amount=request.form.get('amount')
        if accountid:
            a_user = Accounts.query.filter(and_(Accounts.accountid==accountid,Accounts.status=='Active')).first()
            if a_user:
                balance=a_user.balance
                new_balance=balance+int(amount)
                a_user.balance=new_balance
                tt=Transactions(customerid=a_user.customerid,accountid=accountid,amount=amount,msg='credit',date=datetime.datetime.now())
                db.session.add(tt)
                db.session.commit()
                flash('Transaction successful')
                return render_template('display1.html',account=a_user)
            else:
                flash('Account ID invalid/ Inactive Account')
        
    return render_template('deposit.html')


#withdraw
@app.route('/withdraw',methods=['GET','POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        accountid = request.form.get('accountid')
        amount=request.form.get('amount')
        amount=int(amount)
        if accountid:
            a_user = Accounts.query.filter(and_(Accounts.accountid==accountid,Accounts.status=='Active')).first()
            if a_user:
                balance=a_user.balance
                if(balance>=amount):
                    new_balance=balance-amount
                    a_user.balance=new_balance
                    tt=Transactions(accountid=accountid,customerid=a_user.customerid,amount=amount,msg='debit',date=datetime.datetime.now())
                    db.session.add(tt)
                    db.session.commit()
                    flash('Transaction successful')
                    return render_template('display1.html',account=a_user)
                else:
                    flash('Insufficient balance')
            else:
                flash('Account Id Invalid or inactive account !')
    return render_template('withdraw.html')

#transfer
@app.route('/transfer',methods=['GET','POST'])
@login_required
def transfer():
    if request.method == 'POST':
        SA= request.form.get('SA')
        TA= request.form.get('TA')
        amount=request.form.get('amount')
        amount=int(amount)
        if SA:
            if TA:
                SA_user = Accounts.query.filter(and_(Accounts.accountid==SA,Accounts.status=='Active')).first()
                if SA_user:
                    TA_user = Accounts.query.filter(and_(Accounts.accountid==TA,Accounts.status=='Active')).first()
                    if TA_user:
                        SA_balance=SA_user.balance
                        if SA_balance>=amount:
                            new_SA_balance=SA_balance-amount
                            SA_user.balance=new_SA_balance
                            tt=Transactions(accountid=SA,customerid=SA_user.accountid,amount=amount,msg='transfered-to '+str(TA),date=datetime.datetime.now())
                            db.session.add(tt)
                            TA_balance=TA_user.balance
                            new_TA_balance=TA_balance+amount
                            TA_user.balance=new_TA_balance
                            tt=Transactions(accountid=TA,customerid=TA_user.customerid,amount=amount,msg='received from '+str(SA),date=datetime.datetime.now())
                            db.session.add(tt)
                            db.session.commit()
                            flash('Transaction successful')
                            return render_template('display2.html',SA=SA,TA=TA,SA_balance=SA_balance,TA_balance=TA_balance,new_SA_balance=new_SA_balance,new_TA_balance=new_TA_balance)
                        else:
                            flash('Insufficent balance')
                    else:
                        flash('Target Account not Found/ Inactive')        
                else:
                    flash('Source Account not found/ Inactive ')    
            else:
                flash('please enter Target account') 
        else:
            flash('please enter Source account')  
    return render_template('transfer.html')

@app.route('/statement',methods=['GET','POST'])
@login_required
def statement():
    if request.method=='POST' and 'fdate' in request.form:
        accountid=request.form.get('accountid')
        fdate=request.form.get('fdate')
        tdate=request.form.get('tdate')
        qry =Transactions.query.filter(and_(Transactions.date.between(fdate, tdate),Transactions.accountid==accountid)).all()
        if qry:
            return render_template('transactions.html',fdate=fdate,tdate=tdate,transactions=qry)
        else:
            flash('NO Transactions Exists')
            return redirect(url_for('statement'))
    if request.method=='POST' and 'nots' in request.form:
        nots=request.form.get('nots')
        accountid=request.form.get('accountid')
        entities = Transactions.query.order_by(desc(Transactions.date)).filter_by(accountid=accountid).limit(nots)
        if entities:
            return render_template('transactions.html',transactions=entities)
        else:
            flash('NO Transactions Exists')
            return redirect(url_for('statement'))
    else:
        return render_template('statement.html')