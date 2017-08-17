from flask import redirect, url_for, render_template, request, jsonify
import sys 
sys.path.append('.')
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from AppDB import createDB
from helpers import *
db=createDB()

class Lunch:
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
                try:
                    result=History.LunchHistory(reg_no=session['reg_no'],base=countItem1.item,veg=countItem2.item,nonveg="NULL")
                except:
                    result=History.LunchHistory(reg_no=session['reg_no'],base=countItem1.item, nonveg=countItem3.item,veg="NULL")
                    
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
                
                db.add(result)
                db.commit()
                
                return redirect(url_for("index"))
            except:
                db.rollback()
                return apology("Something went wrong")