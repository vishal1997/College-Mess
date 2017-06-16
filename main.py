from flask import Flask, redirect, url_for, render_template, flash, request, jsonify
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from helpers import *
from flask_session import Session
from time import sleep
engine = create_engine('sqlite:///messmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
db = DBsession()

app=Flask(__name__)
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




@app.route("/")
@app.route("/index")
@login_required
def index():
    reset()
    return apology("TODO")

def reset():
    today=date.today()
    print("RESET")
    try :
        added_date = db.query(VegItem.time).filter_by(id="1").one()   
    except:
        print("No Items found")
        return
        
    if today.day > added_date[0].day:
        try:
            num_rows_deleted = db.query(VegItem).delete()
            db.commit()
            num_rows_deleted = db.query(BaseItem).delete()
            db.commit()
            num_rows_deleted = db.query(NonVegItem).delete()
            db.commit()
            ss=db.query(Student).all()
            for s in ss:
                s.checked=0
                db.add(s)
                db.commit()
        except:
            return apology("No menu found")

@app.route("/breakfast/<int:dateId>/", methods=["GET","POST"])
@login_required
def breakfast(dateId):
    if request.method=="POST":
        item1=0
        item2=0
        item3=0
        item4=0
        
        student1=db.query(Student).filter_by(reg_no=session["reg_no"]).one()
        if student1.checked==1 or student1.checked_bf==1:
            return apology("Already Selected Your Choice")
        reg_no=db.query(Bill).filter_by(reg_no=session['reg_no']).one()
        
        try:
            item1=db.query(BFMenu1).filter_by(item=request.form["menu1"]).one()
            reg_no.total_bill += item1.price
        except:
            return apology("Select from menu 1")
        
        try:
            item2=db.query(BFMenu2).filter_by(item=request.form["menu2"]).one()
            reg_no.total_bill += item2.price
        except:
            return apology("Select from menu 2")
            
        try:
            item3=db.query(BFMenu3).filter_by(item=request.form["menu3"]).one()
            reg_no.total_bill += item3.price
        except:
            return apology("Select from menu 3")
            
        
        try:
            item4=db.query(BFMenu4).filter_by(item=request.form["menu4"]).one()
            reg_no.total_bill += item4.price
        except:
            return apology("Select from menu 4")
        
        try:
            item1.count += 1
            db.add(item1)
            db.commit()
            
            item2.count += 1
            db.add(item2)
            db.commit()
            
            item3.count += 1
            db.add(item3)
            db.commit()
            
            item4.count += 1
            db.add(item4)
            db.commit()
            
            db.add(reg_no)
            db.commit()
            
            student1.checked_bf=1
            db.add(student1)
            db.commit()
            """try:
                result=History(reg_no=session['reg_no'],base=countItem1.item,veg=countItem2.item,nonveg="NULL")
            except:
                result=History(reg_no=session['reg_no'],base=countItem3.item, nonveg=countItem3.item,veg="NULL")
            db.add(result)
            db.commit()"""
            return redirect(url_for("index"))
        except:
            db.rollback()
            return apology("Something went wrong")
        
        
        
    else:
        menu1=db.query(BFMenu1).all()
        menu2=db.query(BFMenu2).all()
        menu3=db.query(BFMenu3).all()
        menu4=db.query(BFMenu4).all()
        return render_template("breakfast.html",dateId=dateId, menu1_items=menu1, menu2_items=menu2, menu3_items=menu3, menu4_items=menu4)


@app.route('/lunch/<int:dateId>/', methods=["GET","POST"])
@login_required
def lunch(dateId):
    if request.method=='GET':
        try:
            veg_items=db.query(VegItemLunch).all()
            nonveg_items=db.query(NonVegItemLunch).all()
            base_items=db.query(BaseItemLunch).all()
        except:
            return apology("No data found")
        return render_template("lunch.html",veg_items=veg_items,nonveg_items=nonveg_items,base_items=base_items,dateId=dateId)
    else:
        countItem1=0
        countItem2=0
        countItem3=0
        student1=db.query(Student).filter_by(reg_no=session["reg_no"]).one()
        if student1.checked==1 or student1.checked_ln==1:
            return apology("Already Selected Your Choice")
        try:
            countItem1=db.query(BaseItemLunch).filter_by(item=request.form["base"]).one()
        except:
            return apology("Select a base item")
        
        reg_no=db.query(Bill).filter_by(reg_no=session['reg_no']).one()
        try:
            try:
                countItem2=db.query(VegItemLunch).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem2.price
                countItem3="NULL"
            except:
                countItem3=db.query(NonVegItemLunch).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem3.price
                countItem2="NULL"
        except:
            return apology("Select a menu from veg or non-veg")
            
        
        reg_no.total_bill += countItem1.price
        
        try:
            countItem1.count += 1
            db.add(countItem1)
            db.commit()

            try:
                countItem2.count += 1
                db.add(countItem2)
                db.commit()
            except:
                countItem3.count += 1
                db.add(countItem3)
                db.commit()
            db.add(reg_no)
            db.commit()
            
            student1.checked_ln=1
            db.add(student1)
            db.commit()
            try:
                result=History(reg_no=session['reg_no'],base=countItem1.item,veg=countItem2.item,nonveg="NULL")
            except:
                result=History(reg_no=session['reg_no'],base=countItem3.item, nonveg=countItem3.item,veg="NULL")
            db.add(result)
            db.commit()
            return redirect(url_for("index"))
        except:
            db.rollback()
            return apology("Something went wrong")
            

@app.route('/dinner/<int:dateId>/', methods=["GET","POST"])
@login_required
def dinner(dateId):
    if request.method=='GET':
        try:
            veg_items=db.query(VegItemDinner).all()
            nonveg_items=db.query(NonVegItemDinner).all()
            base_items=db.query(BaseItemDinner).all()
        except:
            return apology("No data found")
        return render_template("dinner.html",veg_items=veg_items,nonveg_items=nonveg_items,base_items=base_items,dateId=dateId)
    else:
        countItem1=0
        countItem2=0
        countItem3=0
        student1=db.query(Student).filter_by(reg_no=session["reg_no"]).one()
        if student1.checked==1 or student1.checked_dn==1:
            return apology("Already Selected Your Choice")
        try:
            countItem1=db.query(BaseItemDinner).filter_by(item=request.form["base"]).one()
        except:
            return apology("Select a base item")
        
        reg_no=db.query(Bill).filter_by(reg_no=session['reg_no']).one()
        try:
            try:
                countItem2=db.query(VegItemDinner).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem2.price
                countItem3="NULL"
            except:
                countItem3=db.query(NonVegItemDinner).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem3.price
                countItem2="NULL"
        except:
            return apology("Select a menu from veg or non-veg")
            
        
        reg_no.total_bill += countItem1.price
        
        try:
            countItem1.count += 1
            db.add(countItem1)
            db.commit()

            try:
                countItem2.count += 1
                db.add(countItem2)
                db.commit()
            except:
                countItem3.count += 1
                db.add(countItem3)
                db.commit()
            db.add(reg_no)
            db.commit()
            
            student1.checked_dn=1
            db.add(student1)
            db.commit()
            try:
                result=History(reg_no=session['reg_no'],base=countItem1.item,veg=countItem2.item,nonveg="NULL")
            except:
                result=History(reg_no=session['reg_no'],base=countItem3.item, nonveg=countItem3.item,veg="NULL")
            db.add(result)
            db.commit()
            return redirect(url_for("index"))
        except:
            db.rollback()
            return apology("Something went wrong")
            
 
    
    
@app.route('/snacks/<int:dateId>/', methods=["GET","POST"])
@login_required
def snacks(dateId):
    return apology("Not yet completed")     
    
    

    

@app.route("/choice", methods=["GET","POST"])
@login_required
def choice():
    if request.method=="POST":
        if request.form.get("breakfast1"):
            return redirect(url_for('breakfast',dateId=1))
            
        elif request.form.get("lunch1"):
            return redirect(url_for('lunch', dateId=1))
            
        elif request.form.get("snacks1"):
            return redirect(url_for('snacks', dateId=1))
            
        elif request.form.get("dinner1"):
            return redirect(url_for('dinner', dateId=1))
            
        elif request.form.get("breakfast2"):
            return redirect(url_for('breakfast',dateId=2))
            
        elif request.form.get("lunch2"):
            return redirect(url_for('lunch', dateId=2))
            
        elif request.form.get("snacks2"):
            return redirect(url_for('snacks',dateId=2))
            
        elif request.form.get("dinner2"):
            return redirect(url_for('dinner', dateId=2))
        else:
            return apology("Something went wrong")
            
    else:
        return render_template("choice.html")

@app.route("/select", methods=["GET", "POST"])
@login_required
def select():
    if request.method=='GET':
        try:
            veg_items=db.query(VegItem).all()
            nonveg_items=db.query(NonVegItem).all()
            base_items=db.query(BaseItem).all()
        except:
            return apology("No data found")
        return render_template("select.html",veg_items=veg_items,nonveg_items=nonveg_items,base_items=base_items)
    else:
        countItem1=0
        countItem2=0
        countItem3=0
        student1=db.query(Student).filter_by(reg_no=session["reg_no"]).one()
        if student1.checked==1:
            return apology("Already Selected Your Choice")
        try:
            countItem1=db.query(BaseItem).filter_by(item=request.form["base"]).one()
        except:
            return apology("Select a base item")
        
        reg_no=db.query(Bill).filter_by(reg_no=session['reg_no']).one()
        try:
            try:
                countItem2=db.query(VegItem).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem2.price
                countItem3="NULL"
            except:
                countItem3=db.query(NonVegItem).filter_by(item=request.form["mainmenu"]).one()
                reg_no.total_bill += countItem3.price
                countItem2="NULL"
        except:
            return apology("Select a menu from veg or non-veg")
            
        
        reg_no.total_bill += countItem1.price
        
        try:
            countItem1.count += 1
            db.add(countItem1)
            db.commit()

            try:
                countItem2.count += 1
                db.add(countItem2)
                db.commit()
            except:
                countItem3.count += 1
                db.add(countItem3)
                db.commit()
            db.add(reg_no)
            db.commit()
            
            student1.checked=1
            db.add(student1)
            db.commit()
            try:
                result=History(reg_no=session['reg_no'],base=countItem1.item,veg=countItem2.item,nonveg="NULL")
            except:
                result=History(reg_no=session['reg_no'],base=countItem3.item, nonveg=countItem3.item,veg="NULL")
            db.add(result)
            db.commit()
            return redirect(url_for("index"))
        except:
            db.rollback()
            return apology("Something went wrong")
        
        
        


@app.route("/history")
@login_required
def history():
    """Show history."""
    mess_history=db.query(History).filter_by(reg_no=session['reg_no']).all()
    return render_template("history.html",mess_history=mess_history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("reg_no"):
            return apology("must provide registeration number")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        #rows = db.execute("SELECT * FROM student WHERE reg_no = :reg_no", reg_no=request.form.get("reg_no"))
        try:
            rows=db.query(Student).filter_by(reg_no=request.form['reg_no']).one()
        except:
            return apology("User not registered")
        # ensure username exists and password is correct
        if not pwd_context.verify(request.form["password"], rows.password):
            return apology("invalid registration no. and/or password")

        # remember which user has logged in
        session["user_id"] = rows.id
        session["reg_no"]=rows.reg_no
        session["name"]=rows.name

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/demand", methods=["GET", "POST"])
@login_required
def demand():
    """Get stock quote."""
    veg_items=db.query(VegItem).all()
    nonveg_items=db.query(NonVegItem).all()
    base_items=db.query(BaseItem).all()
    return render_template("demand.html",veg_items=veg_items,nonveg_items=nonveg_items,base_items=base_items)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    session.clear()
    if(request.method=="POST"):
        if not request.form.get("reg_no"):
            return apology("You must provide registration number")
        elif not request.form.get("password"):
            return apology("You must provide your password")
        elif not request.form.get("confirm"):
            return apology("Please confirm your password")
        elif request.form.get("password")!= request.form.get("confirm"):
            return apology("Password not matched ")
        #result = db.execute("INSERT INTO student (reg_no,name, password) VALUES(:reg_no , :name, :password)",reg_no=request.form.get("reg_no"), name=request.form.get("name"), password=pwd_context.hash(request.form.get("password")))
        result=Student(reg_no=request.form['reg_no'], name=request.form['name'], password=pwd_context.hash(request.form.get("password")))
        if not result:
            return apology("Already Registered")
        set_bill=Bill(reg_no=request.form['reg_no'])
        db.add(set_bill)
        db.commit()
        try:
            db.add(result)
            db.commit()
        
            session["user_id"]=result.id
            session["name"]=result.name
            session["reg_no"]=result.reg_no
        except:
            db.rollback()
        return redirect(url_for('index'))
    else:
        return render_template("register.html")


@app.route("/bill", methods=["GET","POST"])
@login_required
def bill():
    """Bill till now"""
    try:
        student_bill=db.query(Bill).filter_by(reg_no=session["reg_no"]).all()
    except:
        return redirect(url_for('index'))
    sum=0;
    for i in student_bill:
        sum += i.total_bill
    return render_template("bill.html",student_bill=student_bill,sum=sum)
    

if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug= True        
    app.run(host='0.0.0.0',port=5000)
    
