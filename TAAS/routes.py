from TAAS import app
from flask import render_template, request, session, redirect, url_for
from TAAS import db
from TAAS.models import Customers, Administrator, Car, Journey, Booking, CModel, Statistics
from datetime import datetime

@app.route('/')
def index():
    return render_template('logreg.html')


@app.route('/about')
def About():
    return render_template('about.html')


@app.route('/Contact')
def Contact():
    return render_template('Contact.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/display_page')
def display_page():
    return render_template('display_page.html')


@app.route('/customer_login', methods=["POST", "GET"])
def customer_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        check = request.form.getlist('adminis')
        if len(check) != 0 and check[0] == 'checked':
            admn = Administrator.query.filter_by(uname=username, password=password).first()
            if admn is None: # if admin is not found
                return redirect('/')
            elif password == admn.password:
                # response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                return redirect('/adminstr')
            else: # if password is wrong
                return redirect('/')
        else:
            cust = Customers.query.filter_by(uname=username).first()
            if cust is None:  # if wrong username
                return redirect("/")
            elif password == cust.password:
                # response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                return render_template('customer.html', customer=cust)
            else:  # if password is wrong
                return redirect("/")

    return redirect("/")

@app.route('/customer_register', methods=["POST", "GET"])
def customer_register():
    if request.method == "POST":
        name = request.form['name']
        uname = request.form['uname']
        password = request.form['pswd']
        pjrny = 0
        cust = Customers.query.filter_by(uname=uname)
        for cs in cust:
            if cs.uname == uname:
                return "Username already exists"

        new_customer = Customers(
            name=name, uname=uname, password=password, pjrny=pjrny, jdate=datetime.utcnow())
        db.session.add(new_customer)
        db.session.commit()

    return redirect("/")

@app.route('/adminstr')
def adminstr():
    return render_template('adminstr.html')

@app.route('/carlist')
def carlist():
    cars = Car.query.all()
    return render_template('carlist.html', cars=cars)

@app.route('/customerlist')
def customerlist():
    customers = Customers.query.all()
    return render_template('customerlist.html', customers=customers)

@app.route('/stats')
def stats():
    statlist = Statistics.query.all()
    return render_template('stats.html', statlist=statlist)

@app.route('/addCar',methods= ["POST","GET"])
def add_Car():
    if(request.method == "POST"):
        carname = request.form['carname']
        quantity = int(request.form['quantity'])
        type = request.form['dog-names']
        cost_h = request.form['cost_h']
        cost_k = request.form['cost_k']
        if type == "AC":
            cmdl = CModel(mname=carname, accar=quantity, naccar=0, rent_h=cost_h, rent_k=cost_k)
            db.session.add(cmdl)
            db.session.commit()
            for i in range(quantity):
                car = Car(model=carname, kms=0, ac=True, avl=True, fuel=0)
                db.session.add(car)
                db.session.commit()
        else:
            cmdl = CModel(mname=carname, accar=0, naccar=quantity, rent_h=cost_h, rent_k=cost_k)
            db.session.add(cmdl)
            db.session.commit()
            for i in range(quantity):
                car = Car(model=carname, kms=0, ac=False, avl=True, fuel=0)
                db.session.add(car)
                db.session.commit()
        return redirect('/carlist')

    else:
        return render_template('addCar.html')
        
@app.route('/deleteaccount/<int:sno>')
def deleteaccount(sno):
    customer = Customers.query.filter_by(sno=sno).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

@app.route('/repair_snd')
def repair():
    cars = Car.query.all()
    cmdel = CModel.query.all()
    return render_template('repair_snd.html', cars=cars, cmdel=cmdel)

@app.route('/repair_get')
def repair():
    cars = Car.query.all()
    cmdel = CModel.query.all()
    return render_template('repair_get.html', cars=cars, cmdel=cmdel)

# 0 -> Available, 1 -> Rented, 2 -> Repair
@app.route('/sendrepair/<int:id>')
def sendrepair(id):
    car = Car.query.filter_by(id=id).first()
    mdl = car.model
    cmdl = CModel.query.filter_by(mname=mdl).first()
    if car.ac == True:
        cmdl.accar -= 1
    else:
        cmdl.naccar -= 1
    
    db.sessionadd(cmdl)
    db.session.commit()

    car.avl = 2
    db.session.add(car)
    db.session.commit()
    return redirect('/repaircar')

@app.route('/getrepair/<int:id>')
def getrepair(id):
    car = Car.query.filter_by(id=id).first()
    mdl = car.model
    cmdl = CModel.query.filter_by(mname=mdl).first()
    if car.ac == True:
        cmdl.accar += 1
    else:
        cmdl.naccar += 1
    
    db.sessionadd(cmdl)
    db.session.commit()

    car.avl = 0
    db.session.add(car)
    db.session.commit()
    return redirect('/repair')

@app.route('/change_rent/<int:mno>', methods=["POST", "GET"])
def change_rent(mno):
    if request.method == "POST":
        cmdl = CModel.query.filter_by(mno=mno).first()
        cmdl.rent_h = request.form['rent_h']
        cmdl.rent_k = request.form['rent_k']
        db.session.add(cmdl)
        db.session.commit()
        return redirect('/carlist')
    else:
        cmdl = CModel.query.filter_by(mno=mno).first()
        return render_template('change_rent.html', cmdl=cmdl)