from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Boolean, Float, Table
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db  


# app = Flask(__name__)
# app.secret_key ='soujgpoisefpowigmppwoigvhw0wefwefwogihj'

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
# db = SQLAlchemy(app)


# flag_modified(user_instance, 'modified parameter') when modifying json file; tell database json is modified
def load_default_events():
    with open('static/assets/jsons/default_events.json', 'r') as file:
        default_events = json.load(file)
    return default_events

def load_create_default():
    with open('static/assets/jsons/created_events.json', 'r') as file:
        default_events = json.load(file)
    return default_events

def load_joined_users():
    with open('static/assets/jsons/created_events.json', 'r') as file:
        default_events = json.load(file)
    return default_events

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    email_verification_token = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    mfa_enabled = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(10), nullable=False, default='')
    account_type = db.Column(db.String(255), nullable=False, default="Student")
    joined_events = db.Column(JSON, default = load_default_events)
    


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"ID: {self.id}\nFirst Name: {self.first_name}\nLast Name: {self.last_name}\nEmail: {self.email}\n Account Type {self.__class__.__name__}"

    def create_event(self, **kwargs):
        if not isinstance(self, Teacher):
            raise PermissionError("Only teachers and admins can create events.")
        pass
        # event = Event(**kwargs, creator=self)
        # db.session.add(event)
        # db.session.commit()
        return # event

class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    events_created = db.Column(JSON, default = load_create_default)

class Admin(Teacher):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)

class SuperAdmin(Admin):
    __tablename__ = 's_admin'
    id = db.Column(db.Integer,db.ForeignKey('admin.id'), primary_key=True)

class Event(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, default='null')
    description = db.Column(db.String(350), nullable=False, default='null')
    image = db.Column(db.LargeBinary)
    student_limit = db.Column(db.Integer, nullable = False)
    participants = db.Column(JSON, load_joined_users)


class ProjectWednesday(Event):
    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    cycle_number = db.Column(db.Integer, default=1, nullable=False)

class Tournaments(Event):
    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    cost = db.Column(db.Float, default=1, nullable=False)

