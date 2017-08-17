from flask import redirect, render_template, request,url_for
import sys 
sys.path.append('.')


class Select:
    def select():
        if request.method=="POST":
            if request.form.get("breakfast1"):
                return redirect(url_for('breakfast',dateId=1))
                
            elif request.form.get("lunch1"):
                return redirect(url_for('lunch', dateId=1))
                
            elif request.form.get("snacks1"):
                return redirect(url_for('snacks', dateId=1))
                
            elif request.form.get("dinner1"):
                return redirect(url_for('dinner', dateId=1))
                
            elif request.form.get("breakfast2"):
                return redirect(url_for('breakfast',dateId=2))
                
            elif request.form.get("lunch2"):
                return redirect(url_for('lunch', dateId=2))
                
            elif request.form.get("snacks2"):
                return redirect(url_for('snacks',dateId=2))
                
            elif request.form.get("dinner2"):
                return redirect(url_for('dinner', dateId=2))
            else:
                return apology("Something went wrong")
                
        else:
            return render_template("select.html")