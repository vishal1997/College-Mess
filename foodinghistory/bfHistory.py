from flask import render_template
import sys 
sys.path.append('.')
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from AppDB import createDB
from helpers import *
db=createDB()


class BfHistory:
    def bfHistory(dateId):
        mess_history=db.query(History.BFHistory).filter_by(reg_no=session['reg_no']).all()
        return render_template("bfHistory.html",mess_history=mess_history)   