from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db  # Adjust the import path as necessary


# app = Flask(__name__)
# app.secret_key ='soujgpoisefpowigmppwoigvhw0wefwefwogihj'

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
# db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    email_verification_token = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default = False)
    mfa_enabled = db.Column(db.Boolean, default = False)
    phone_number = db.Column(db.String(10), nullable = False, default = '')
    account_type = db.Column(db.String(255), nullable = False, default = "Student")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"ID: {self.id}\n First Name: {self.first_name}\n Last Name: {self.last_name}\n Email: {self.email}\n Account Type: {self.account_type} "
