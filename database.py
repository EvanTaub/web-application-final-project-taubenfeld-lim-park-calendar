
from flask import Flask, render_template, request, redirect, url_for, flash, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from werkzeug.utils import secure_filename
import csv
from sqlalchemy import desc, asc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.secret_key ='soujgpoisefpowigmppwoigvhw0wefwefwogihj'
oauth = OAuth(app)

# Establish login
login_manager = LoginManager(app)









# Setup the database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
# db = SQLAlchemy(app)

# with app.app_context():
#     db.create_all()