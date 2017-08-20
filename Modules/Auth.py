from flask import redirect, url_for, render_template, request
from flask_session import Session
from dataBase import Base, Student,Bill
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime, date

import sys 
sys.path.append('.')
from Modules.Util import Util
from helpers import *
from AppDB import createDB
db=createDB()



class Auth:
	def index():
		Util.reset()


	def login():
		# forget any user_id
		session.clear()

		# if user reached route via POST (as by submitting a form via POST)
		if request.method == "POST":

			# ensure username was submitted
			if not request.form.get("reg_no"):
				return apology("must provide registeration number")

			# ensure password was submitted
			elif not request.form.get("password"):
				return apology("must provide password")

			# query database for username
			#rows = db.execute("SELECT * FROM student WHERE reg_no = :reg_no", reg_no=request.form.get("reg_no"))
			try:
				rows=db.query(Student).filter_by(reg_no=request.form['reg_no']).one()
			except:
				return apology("User not registered")
			# ensure username exists and password is correct
			if not pwd_context.verify(request.form["password"], rows.password):
				return apology("invalid registration no. and/or password")

			# remember which user has logged in
			session["user_id"] = rows.id
			session["reg_no"]=rows.reg_no
			session["name"]=rows.name

			# redirect user to home page
			return redirect(url_for("index"))

		# else if user reached route via GET (as by clicking a link or via redirect)
		else:
			return render_template("login.html")

	def logout():
		# forget any user_id
		session.clear()

		# redirect user to login form
		return redirect(url_for("login"))

	def register():
		"""Register user."""
		session.clear()
		if(request.method=="POST"):
			if not request.form.get("reg_no"):
				return apology("You must provide registration number")
			elif not request.form.get("password"):
				return apology("You must provide your password")
			elif not request.form.get("confirm"):
				return apology("Please confirm your password")
			elif request.form.get("password")!= request.form.get("confirm"):
				return apology("Password not matched ")
			#result = db.execute("INSERT INTO student (reg_no,name, password) VALUES(:reg_no , :name, :password)",reg_no=request.form.get("reg_no"), name=request.form.get("name"), password=pwd_context.hash(request.form.get("password")))
			result=Student(reg_no=request.form['reg_no'], name=request.form['name'], password=pwd_context.hash(request.form.get("password")))
			if not result:
				return apology("Already Registered")
			set_bill=Bill(reg_no=request.form['reg_no'])
			db.add(set_bill)
			db.commit()
			try:
				db.add(result)
				db.commit()
			
				session["user_id"]=result.id
				session["name"]=result.name
				session["reg_no"]=result.reg_no
			except:
				db.rollback()
			return redirect(url_for('index'))
		else:
			return render_template("register.html")

				
				