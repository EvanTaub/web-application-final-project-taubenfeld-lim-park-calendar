from flask import Flask, render_template, flash, url_for, request, redirect
import re
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

#temporary route for proof of concept
@app.route('/eventsday1')
def eventsday1():
    return render_template('sampledate.html')



# edit / add / profile 

if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)