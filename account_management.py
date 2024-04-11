from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required, UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from classes import User

from extensions import db  # Adjust the import path as necessary



def register_main():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    password = request.form.get('password')
    verify_password = request.form.get('v_password')
    user = User.query.filter_by(email = email).first()
    print(user)
    if user:
        flash('User with this email already Exists!', 'warning')
        return redirect(url_for('register'))
    if password != verify_password:
        flash('Passwords are not the same','danger')
        return redirect(url_for('register'))
    
    new_user = User(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password_hash = generate_password_hash(password)
    )
    return (new_user)
        

def login_management():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    print(user)
    print(user.check_password(password))
    if user and user.check_password(password):
        print("True")
        login_user(user)
        flash("Logged in successfully!", 'success')
        return render_template('index.html')
    

def load_user_main(user_id):
    return User.query.get(int(user_id))

def logout_main():
    logout_user()
    flash("Successfully Logged Out!", 'success')
    
