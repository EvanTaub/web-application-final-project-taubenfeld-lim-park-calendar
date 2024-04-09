from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def configure_app():
    global app
    app = Flask(__name__)
    app.secret_key ='soujgpoisefpowigmppwoigvhw0wefwefwogihj'

    # Establish login
    global login_manager
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Unauthorized Access. Please Login!"
    login_manager.login_message_category = 'danger'


    # Setup the database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar.db"
    global db
    db = SQLAlchemy(app)
