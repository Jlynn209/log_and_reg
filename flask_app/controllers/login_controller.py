# you need to import from the app
# you need to import the following from flask to render, redirect, request, session, and flash. <--- anything that controls what the front-end user will see or go to.
# you will need to import your model associated with the controller.

from re import template
from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models import login_model

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create" ,methods=['POST'])
def create_user():
    if request.form['pw'] != request.form['confirm_pw']:
        flash("Passwords do not match!")
        return redirect("/")
    
    user_in_db = login_model.Users.get_one_email({'email':request.form['email']})
    if (user_in_db):
        flash("Email already exist for this website!")

    if not login_model.Users.validate_reg(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['pw'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "pw" : pw_hash
    }

    login_model.Users.create(data)
    return redirect("/")

@app.route("/login", methods=['POST'])
def login():

    if len(request.form['pw']) < 1 or len(request.form['email']) < 1:
        flash("Please enter a valid email and password")
        return redirect("/")

    data = {
        "email": request.form['email']
    }

    user_in_db = login_model.Users.get_one_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.pw, request.form['pw']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id

    return redirect("/logged")

@app.route("/logged")
def logged():
    if 'user_id' not in session:
        return redirect("/")
    user = login_model.Users.get_one({'id':session['user_id']})
    return render_template("logged.html", user = user)

@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect("/")