from flask import redirect, render_template, request
import sys 
sys.path.append('.')
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from AppDB import createDB
from helpers import *
db=createDB()

class Demand:
    def demand():
        if request.method=="POST":
            snacks1=db.query(Snack1).all()
            snacks2=db.query(Snack2).all()
            bfmenu1=db.query(BFMenu1).all()
            bfmenu2=db.query(BFMenu2).all()
            bfmenu3=db.query(BFMenu3).all()
            bfmenu4=db.query(BFMenu4).all()
            return render_template("snacksBF.html",snacks1=snacks1, snacks2=snacks2,bfmenu1=bfmenu1,bfmenu2=bfmenu2,bfmenu3=bfmenu3,bfmenu4=bfmenu4)    
            
            
        veg_items_d=db.query(VegItemDinner).all()
        nonveg_items_d=db.query(NonVegItemDinner).all()
        base_items_d=db.query(BaseItemDinner).all()
        
        veg_items_l=db.query(VegItemLunch).all()
        nonveg_items_l=db.query(NonVegItemLunch).all()
        base_items_l=db.query(BaseItemLunch).all()

        return render_template("demand.html",veg_items_d=veg_items_d,nonveg_items_d=nonveg_items_d,base_items_d=base_items_d,veg_items_l=veg_items_l,nonveg_items_l=nonveg_items_l,base_items_l=base_items_l)
        