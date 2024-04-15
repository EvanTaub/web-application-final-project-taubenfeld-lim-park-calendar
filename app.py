from flask import Flask, render_template, request, redirect, url_for, flash, session


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from werkzeug.utils import secure_filename
import csv
from sqlalchemy import desc, asc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import base64, io
from PIL import Image


import random
# twilio test


from twilio.rest import Client

from database import login_manager
from account_management import login_management, logout_main, register_main, load_user_main
from classes import User

from extensions import db, login_manager  # Adjust the import path as necessary


app = Flask(__name__)
app.config['SECRET_KEY'] = 'soujgpoisefpowigmppwoigvhw0wefwefwogihj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Unauthorized Access. Please Login!"
login_manager.login_message_category = 'danger'


with app.app_context():
    db.create_all()

# Here you can register your blueprints or routes












# def generate_verification_token():
#     return secrets.token_urlsafe(50)  # Adjust the token length as needed


# # Send a Verification Email:
# def send_verification_email(user):
#     verification_link = (
#         f"http://127.0.0.1:5000/verify_email/{user.email_verification_token}"
#     )
#     msg = Message("Verify Your Email", recipients=[user.email])
#     msg.body = f"Click the following link to verify your email: {verification_link}"
#     mail.send(msg)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        register_item = register_main()
        if isinstance(register_item,User):
            db.session.add(register_item)
            db.session.commit()
        else:
            flash(register_item[0],register_item[1])
            return redirect(url_for('register'))
        return redirect(url_for('index'))

        

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html") 
    if request.method == "POST":
        var = login_management()
        if var[0]:
            login_user(var[1])
            flash('Logged In Successfully!','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials','danger')
            return redirect(url_for('login'))
        

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_main()
    return redirect(url_for('index'))


@app.route('/events')
def Event():
    return render_template('events.html')


@app.route("/edit")
# @login_required
def edit():
    return render_template("edit.html")

@app.route('/verify_email')
def email_verification():
    pass


# edit / add / profile 

if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)