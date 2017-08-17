from flask import redirect, url_for, render_template, request, jsonify
import sys 
sys.path.append('.')
from dataBase import Base, Student, History,Bill,BFMenu1,BFMenu2,BFMenu3,BFMenu4, Snack1,Snack2,NonVegItemLunch,NonVegItemDinner,VegItemLunch,VegItemDinner,BaseItemLunch,BaseItemDinner
from AppDB import createDB
from helpers import *
db=createDB()

class Snacks:
    def snacks(dateId):
        if request.method=="POST":
            item1=0
            item2=0
            
            student1=db.query(Student).filter_by(reg_no=session["reg_no"]).one()
            if student1.checked==1 or student1.checked_sn==1:
                return apology("Already Selected Your Choice")
            reg_no=db.query(Bill).filter_by(reg_no=session['reg_no']).one()
            
            try:
                item1=db.query(Snack1).filter_by(item=request.form["snack1"]).one()
                reg_no.total_bill += item1.price
            except:
                return apology("Select from menu 1")
            
            try:
                item2=db.query(Snack2).filter_by(item=request.form["snack2"]).one()
                reg_no.total_bill += item2.price
            except:
                return apology("Select from menu 2")
                
            
            try:
                
                try:
                    result=History.SnacksHistory(reg_no=session['reg_no'],sn1=item1.item,sn2=item2.item)
                except:
                    return apology("Error while updating history")
                
                item1.count += 1
                db.add(item1)
                db.commit()
                
                item2.count += 1
                db.add(item2)
                db.commit()
                
                db.add(reg_no)
                db.commit()
                
                student1.checked_sn=1
                db.add(student1)
                db.commit()
                

                db.add(result)
                db.commit()
                return redirect(url_for("index"))
            except:
                db.rollback()
                return apology("Something went wrong")
            
            
            
        else:
            sn1=db.query(Snack1).all()
            sn2=db.query(Snack2).all()
            return render_template("snacks.html",dateId=dateId, menu1_items=sn1, menu2_items=sn2)
        
        
        

    