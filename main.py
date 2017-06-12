from flask import Flask, redirect, url_for, render_template, flash, request, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from dataBase import Base, NonVegItem, VegItem,BaseItem, Student
from helpers import *
from flask_session import Session
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

#db=SQL("sqlite:///messmenu.db")

@app.route("/")
@app.route("/index")
@login_required
def index():
    return apology("TODO")

@app.route("/select", methods=["GET", "POST"])
@login_required
def select():
    """Buy shares of stock."""
    if request.method=='GET':
        veg_items=db.query(VegItem).all()
        nonveg_items=db.query(NonVegItem).all()
        base_items=db.query(BaseItem).all()
        return render_template("select.html",veg_items=veg_items,nonveg_items=nonveg_items,base_items=base_items)
    else:
        countItem1=0
        countItem2=0
        countItem3=0
        try:
            countItem1=db.query(BaseItem).filter_by(item=request.form["base"]).one()
        except:
            return apology("Select a base item")
        try:
            try:
                countItem2=db.query(VegItem).filter_by(item=request.form["mainmenu"]).one()
            except:
                countItem3=db.query(NonVegItem).filter_by(item=request.form["mainmenu"]).one()
        except:
            return apology("Select a menu from veg or non-veg")
        
        try:
            countItem1.count += 1
            db.add(countItem1)
            db.commit()
        except:
            return apology("Something went wrong in selecting base menu. Please try again")
        
        try:
            countItem2.count += 1
            db.add(countItem2)
            db.commit()
        except:
            try:
                countItem3.count += 1
                db.add(countItem3)
                db.commit()
            except:
                return apology("Something went wrong in selecting main menu. Please try again")
        return redirect(url_for("index"))
    #return apology("TODO")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

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
        db.add(result)
        db.commit()
        session["user_id"]=result.id;
        return redirect(url_for('index'))
    else:
        return render_template("register.html")

@app.route("/choice", methods=["GET", "POST"])
@login_required
def choice():
    """Sell shares of stock."""
    return apology("TODO")

@app.route("/bill", methods=["GET","POST"])
@login_required
def bill():
    """Bill till now"""
    return apology("TODO")

if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug= True
    app.run(host='0.0.0.0',port=5000)