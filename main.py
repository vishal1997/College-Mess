from cs50 import SQL
from flask import Flask, redirect, url_for, render_template, flash, request, jsonify

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from dataBase import Base, NonVegItem, VegItem,BaseItem, Student
from helpers import *
from flask_session import Session
"""engine = create_engine('sqlite:///messmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
db = DBsession()
"""
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

db=SQL("sqlite:///messmenu.db")

@app.route("/")
@login_required
def index():
    return apology("TODO")

@app.route("/select", methods=["GET", "POST"])
@login_required
def select():
    """Buy shares of stock."""
    return apology("TODO")

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
        rows = db.execute("SELECT * FROM student WHERE reg_no = :reg_no", reg_no=request.form.get("reg_no"))
        #rows=db.query(Student).filter_by(reg_no=request.form['reg_no'],password=request.form['password']).one()
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form["password"], rows[0]["password"]):
            return apology("invalid registration no. and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    return apology("TODO")

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
        result = db.execute("INSERT INTO student (reg_no,name, password) VALUES(:reg_no , :name, :password)",reg_no=request.form.get("reg_no"), name=request.form.get("name"), password=request.form.get("password"))
                             
        if not result:
            apology("Already Registered")
        session["user_id"]=result;
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