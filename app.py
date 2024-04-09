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


from account_management import login_main, logout_main, register_main

from database import configure_app

configure_app()










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



@app.route("/register", methods = ["GET","POST"])
def register():
    register_main()

        

@app.route("/login", methods = ["GET", "POST"])
def login():
    login_main()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_main()

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