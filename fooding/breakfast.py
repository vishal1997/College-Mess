from flask import redirect, url_for, render_template, request, jsonify
import sys 
sys.path.append('.')
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from AppDB import createDB
from helpers import *
db=createDB()

class BreakFast:
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
                try:
                    result=History.BFHistory(reg_no=session['reg_no'],bfast1=item1.item,bfast2=item2.item,bfast3=item3.item, bfast4= item4.item)
                except:
                    return apology("Error while updating breakfast history ")
                    
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
                
                db.add(result)
                db.commit()
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
