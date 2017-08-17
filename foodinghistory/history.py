from flask import redirect, url_for, render_template, request
import sys 
sys.path.append('.')

class History:
    def history():
        """Show history."""
        if request.method=="POST":
            if request.form.get("breakfast1"):
                return redirect(url_for('bfHistory',dateId=1))
                
            elif request.form.get("lunch1"):
                return redirect(url_for('lnHistory', dateId=1))
                
            elif request.form.get("snacks1"):
                return redirect(url_for('snHistory', dateId=1))
                
            elif request.form.get("dinner1"):
                return redirect(url_for('dnHistory', dateId=1))
                
            elif request.form.get("breakfast2"):
                return redirect(url_for('bfHistory',dateId=2))
                
            elif request.form.get("lunch2"):
                return redirect(url_for('lnHistory', dateId=2))
                
            elif request.form.get("snacks2"):
                return redirect(url_for('snHistory',dateId=2))
                
            elif request.form.get("dinner2"):
                return redirect(url_for('dnHistory', dateId=2))
            else:
                return apology("Something went wrong")
            
            """mess_history=db.query(History.DinnerHistory).filter_by(reg_no=session['reg_no']).all()
            return render_template("history.html",mess_history=mess_history)"""
        else:
            return render_template("history.html")