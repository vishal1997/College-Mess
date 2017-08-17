from flask import redirect, render_template,url_for
import sys 
sys.path.append('.')
from AppDB import createDB
from dataBase import Bill
from helpers import *
db=createDB()

class TotalBill:
    def bill():
        try:
            student_bill=db.query(Bill).filter_by(reg_no=session["reg_no"]).all()
        except:
            return redirect(url_for('index'))
        sum=0
        for i in student_bill:
            sum += i.total_bill
        return render_template("bill.html",student_bill=student_bill,sum=sum)