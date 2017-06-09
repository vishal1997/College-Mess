from flask import Flask, redirect, url_for, render_template, flash, request, jsonify
app=Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from dataBase import Base, NonVegItem, VegItem,BaseItem
from helpers import *

engine = create_engine('sqlite:///messmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
db = DBsession()

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
        #rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        rows=db.query(Student).filter_by(reg_no=request.form['reg_no']).one()
        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
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
    return apology("TODO")

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