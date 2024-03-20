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

# Setup the database
app["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
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


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        email = request.form.get('email')
    return render_template("login.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


@app.route("/edit")
# @login_required
def edit():
    return render_template("edit.html")


# edit / add / profile 

if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)