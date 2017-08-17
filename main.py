from flask import Flask, redirect, url_for, render_template, flash, request, jsonify
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from helpers import *
from flask_session import Session
from time import sleep
from Modules.Auth import Auth
from Modules.Util import Util

from AppDB import createDB



from fooding.Fooding import BreakFast
from fooding.Fooding import Lunch
from fooding.Fooding import Dinner
from fooding.Fooding import Snacks
from foodinghistory.FoodingHistory import FoodingHistory

from fooding.Fooding import Fooding


db=createDB()

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
    Auth.index()
    return apology("TODO")

    
@app.route("/breakfast/<int:dateId>/", methods=["GET","POST"])
@login_required
def breakfast(dateId):
     return BreakFast.breakfast(dateId)
   
    

@app.route('/lunch/<int:dateId>/', methods=["GET","POST"])
@login_required
def lunch(dateId):
    return Lunch.lunch(dateId)
            

@app.route('/dinner/<int:dateId>/', methods=["GET","POST"])
@login_required
def dinner(dateId):
    return Dinner.dinner(dateId)
            
 
    
    
@app.route('/snacks/<int:dateId>/', methods=["GET","POST"])
@login_required
def snacks(dateId):
   return Snacks.snacks(dateId)

@app.route("/select", methods=["GET","POST"])
@login_required
def select():
    return Fooding.select()

@app.route("/history/breakfast/<int:dateId>", methods=["POST","GET"])
@login_required
def bfHistory(dateId):
   return FoodingHistory.bfHistory(dateId)
    

    
@app.route("/history/lunch/<int:dateId>", methods=["POST","GET"])
@login_required
def lnHistory(dateId):
    return FoodingHistory.lnHistory(dateId)
   
   
    
    
@app.route("/history/dinner/<int:dateId>", methods=["POST","GET"])
@login_required
def dnHistory(dateId):
    return FoodingHistory.dnHistory(dateId)
    

@app.route("/history/snacks/<int:dateId>", methods=["POST","GET"])
@login_required
def snHistory(dateId):
    return FoodingHistory.snHistory(dateId)
    
    
    

@app.route("/history", methods=["POST","GET"])
@login_required
def history():
    return FoodingHistory.history()
   

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    return Auth.login()
    

@app.route("/logout")
def logout():
    """Log user out."""
    return Auth.logout()
    

    

@app.route("/demand", methods=["GET", "POST"])
@login_required
def demand():
    return Fooding.demand()



@app.route("/register", methods=["GET", "POST"])
def register():
    return Auth.register()

@app.route("/bill", methods=["GET","POST"])
@login_required
def bill():
    """Bill till now"""
    return Fooding.bill()
    

if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug= True        
    app.run(host='0.0.0.0',port=5000)
    
