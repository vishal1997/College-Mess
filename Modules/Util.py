from flask import Flask, redirect, url_for, render_template, flash, request, jsonify
from helpers import *
from datetime import datetime, date
import sys 
sys.path.append('.')

class Util:
    def reset():
        today=date.today()
        print("RESET")
        try:
            added_date = db.query(VegItemDinner.time).filter_by(id="1").one()   
        except:
            return apology("No Items found")
            
        if today.day > added_date[0].day:
            try:
                num_rows_deleted = db.query(VegItemLunch).delete()
                db.commit()
                num_rows_deleted = db.query(BaseItemLunch).delete()
                db.commit()
                num_rows_deleted = db.query(NonVegItemLunch).delete()
                db.commit()
                
                num_rows_deleted = db.query(VegItemDinner).delete()
                db.commit()
                num_rows_deleted = db.query(BaseItemDinner).delete()
                db.commit()
                num_rows_deleted = db.query(NonVegItemDinner).delete()
                db.commit()
                
                num_rows_deleted = db.query(BFMenu1).delete()
                db.commit()
                num_rows_deleted = db.query(BFMenu2).delete()
                db.commit()
                num_rows_deleted = db.query(BFMenu3).delete()
                db.commit()
                num_rows_deleted = db.query(BFMenu4).delete()
                db.commit()
                
                num_rows_deleted = db.query(Snack1).delete()
                db.commit()
                num_rows_deleted = db.query(Snack2).delete()
                db.commit()
                
                ss=db.query(Student).all()
                for s in ss:
                    s.checked=0
                    db.add(s)
                    db.commit()
            except:
                return apology("No menu found")
