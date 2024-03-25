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
import random
# twilio test
from twilio.rest import Client
import base64, io
from PIL import Image






app = Flask(__name__)
app.secret_key ='soujgpoisefpowigmppwoigvhw0wefwefwogihj'

# Establish login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Unauthorized Access. Please Login!"
login_manager.login_message_category = 'danger'


# Setup the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
db = SQLAlchemy(app)





class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    email_verification_token = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default = False)
    mfa_enabled = db.Column(db.Boolean, default = False)
    phone_number = db.Column(db.String(10), nullable = False)
    account_type = db.Column(db.String(255), nullable = False, default = "Student")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"ID: {self.id}\n First Name: {self.first_name}\n Last Name: {self.last_name}\n Email: {self.email}\n Account Type: {self.account_type} "


with app.app_context():
    db.create_all()



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


@app.route('/edit_event')
def edit_event():
    return render_template('edit_event.html')

#temporary route for proof of concept
@app.route('/eventsday1')
def eventsday1():
    return render_template('sampledate.html')


@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == "POST":
        pass

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", 'success')
            return render_template('index.html')
    return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out!", 'success')
    return redirect(url_for('index'))

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


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