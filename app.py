from flask import Flask, render_template, request, redirect, url_for, flash, session
from authlib.integrations.flask_client import OAuth
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from werkzeug.utils import secure_filename
import csv
from sqlalchemy import desc, asc, not_
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import base64, io
from PIL import Image
from flask_paginate import Pagination
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified
import random
# twilio test


from twilio.rest import Client

from database import login_manager
from account_management import login_management, logout_main, register_main, load_user_main
from classes import User, SuperAdmin, Admin, Teacher, ProjectWednesday, Event, Tournaments,Performances, parse_csv_data, upload_csv_tournaments, upload_csv_wednesday, enter_event, leave_event
#import from classes these old functions? -> join_project_wednesday, attend_performance, enter_tournament_compete, enter_tournament_spectate,

from extensions import db, login_manager  # Adjust the import path as necessary


app = Flask(__name__)
oauth = OAuth(app)
app.config['SECRET_KEY'] = 'soujgpoisefpowigmppwoigvhw0wefwefwogihj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Unauthorized Access. Please Login!"
login_manager.login_message_category = 'danger'

GOOGLE_CLIENT_ID = '867012396004-2orvos6k259l1v8gu8u6ntl9re438fl9.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)



with app.app_context():
    db.create_all()


# with app.app_context():
#     user = SuperAdmin(id = 1, email='redemanjt@gmail.com', first_name='Evan', last_name='Taubenfeld')
#     print(user)
#     db.session.add(user)
#     db.session.commit()

# Here you can register your blueprints or routes
def generate_token():
    return secrets.token_urlsafe(50)  

####### PAGINATION EXAMPLE on back end!!!!!!!!! #######
#  if request.method=='GET':
#         per_page = 5
#         page = request.args.get('page', 1, type=int)
#         offset = (page-1) * per_page
#         # items = get_items(offset)
          
#         pagination = Pagination(page=page, total=Book.query.count(), record_name='items',per_page=per_page)
#         books = Book.query.paginate(page=page,per_page=per_page)
#         return render_template("inventory.html", books = books, pagination=pagination)


@app.route('/google/')
def google():
    page = request.args.get('page')
    session['nonce'] = generate_token()

    print(page)
    # GOOGLE_CLIENT_ID = '867012396004-2orvos6k259l1v8gu8u6ntl9re438fl9.apps.googleusercontent.com'
    # GOOGLE_CLIENT_SECRET = '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'

    # CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    # oauth.register(
    #     name='google',
    #     client_id=GOOGLE_CLIENT_ID,
    #     client_secret=GOOGLE_CLIENT_SECRET,
    #     server_metadata_url=CONF_URL,
    #     client_kwargs={
    #         'scope': 'openid email profile'
    #     }
    # )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

    

@app.route('/google/auth/')
def google_auth():
    try:
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])

        # Retrieve the user's information
        email = user_info.get('email')
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            login_user(existing_user)  # Log them in directly
            session['id'] = existing_user.id
            flash('Logged in successfully through Google!', 'success')
        else:
            # Create a new user if not found
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash='sample_google_password',  # No password set for Google logins
                phone_number='',  # Empty phone number to match model definition
                account_type="Student"  # Default to Student
            )

            # Save the new user to the database
            db.session.add(new_user)
            db.session.commit()

            session['id'] = new_user.id

            login_user(new_user)  # Log the new user in
            flash('Registered and logged in successfully through Google!', 'success')

        # Determine the appropriate page to redirect to
        page = request.args.get('page')
        if page == 'register':
            return redirect(url_for('register'))
        elif page == 'login':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('index'))

    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred during authentication.', 'danger')
        return redirect(url_for('index'))






# google redirect for login http://localhost:5000/google/auth
# client id 867012396004-2orvos6k259l1v8gu8u6ntl9re438fl9.apps.googleusercontent.com
# client secret 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








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

#temporary route
@app.route("/test")
def test():
    return render_template("test.html")




@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    # if request.method == "POST":
    #     register_item = register_main()
    #     if isinstance(register_item,User):
    #         db.session.add(register_item)
    #         db.session.commit()
    #     else:
    #         flash(register_item[0],register_item[1])
    #         return redirect(url_for('register'))
    #     return redirect(url_for('index'))


        

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html") 
    if request.method == "POST":
        var = login_management()
        if var[0]:
            login_user(var[1])
            print(var[1])
            session['id'] = var[1].id
            flash('Logged In Successfully!','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials','danger')
            return redirect(url_for('login'))
        

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))  # Ensure this conversion happens only on valid data
    except (TypeError, ValueError):
        return None  # Return None gracefully for invalid or missing data



@app.route('/logout')
@login_required
def logout():
    logout_main()
    session.pop('id')
    return redirect(url_for('index'))


@app.route('/events', methods = ["GET", "POST"])
def event():
    if request.method == "GET":
        events = Event.query.all() #filter(not_(ProjectWednesday.cycle_number)).all()
        num_events = len(events)
        if num_events == 0:
            flash('There are no events at this time.', 'warning')
            return render_template('index.html')
        # events_per_page = 6
        # page = request.args.get('page', 1, type=int)
        # offset = (page - 1) * events_per_page
        return render_template('view_event_determination.html')
    if request.method == "POST":
        # if "add_event" in request.form:
        #     event_title = request.form.get('event_title')
        #     event_type = request.form.get('event_type')
        #     event_description = request.form.get('event_description')
            
        #     return render_template('events.html')
        # Adds Project Wednesday events in bulk using csv parsing
        if "cycle_submit" in request.form:
            csv_file = request.files["csv_file"]
            csv_data = parse_csv_data(csv_file)
            upload_csv_wednesday(csv_data, current_user.id)
            flash('Events Successfully Added!', 'success')
            return redirect(url_for('event'))
        if "tournament_submit" in request.form:
            process_tournament_data()
            # flash('Events Successfully Added!', 'success')
            return redirect(url_for('event'))
        if "performance_submit" in request.form:
            process_performance_data()
            return redirect(url_for('event'))
        
        if "project_submit" in request.form:
            process_project_data()
            return redirect(url_for('event'))


        # Adds Tournament events in bulk
        if 'tournaments_submit' in request.form:
            csv_file = request.files['csv_file']
            csv_data = parse_csv_data(csv_file)
            upload_csv_tournaments(csv_data)
            flash('Tournaments Added Successfully!', 'success')
            return redirect(url_for('event'))
        if "edit_event" in request.form:
            pass
            return render_template('events.html')
    

        flash('Invalid event submission.', 'error')
        return redirect(url_for('event'))

@app.route('/events/project_wednesday', methods=['GET', 'POST'])
def display_pw():
    projects = ProjectWednesday.query.all() #filter(not_(ProjectWednesday.cycle_number)).all()
    num_events = len(projects)
    if num_events == 0:
        flash('There is no Project Wednesday Cycle to join currently.', 'warning')
        return redirect(url_for('index'))
    if 'event_id' in request.args:
        event_id = request.args.get('event_id')
        project_wednesday = ProjectWednesday.query.get(event_id)

        if request.method == "POST":
            if 'join_button' in request.form:
                if 'id' in session:
                    if current_user.joined_events["Project Wednesday"] != '':
                        flash("You have already joined a Project Wednesday", 'warning')
                        return redirect(url_for('event'))
                    else:
                        enter_event(current_user.id, project_wednesday.id, "Project Wednesday")
                        flash("You have successfully joined the project!", "success")
                else:
                    flash("You must be logged in to make this action!", "danger")
            if 'leave_event' in request.form:
                if 'id' in session:
                    if current_user.joined_events["Project Wednesday"] == "":
                        flash("You have not joined this project!", 'warning')
                        return redirect(url_for('event'))
                    else:
                        leave_event(current_user.id, project_wednesday.id, "Project Wednesday")
                        flash('You have successfully left this event', 'success')
        
        if 'id' in session:
            return render_template('view_pw.html', event = project_wednesday, user= current_user)
        return render_template('view_pw.html', event=project_wednesday, user = '')

    events = ProjectWednesday.query.all()
    return render_template('project_wednesdays.html', events=events)

@app.route('/events/performances', methods=['GET', 'POST'])
def display_performances(): 
    performances = Performances.query.all() #filter(not_(ProjectWednesday.cycle_number)).all()
    num_events = len(performances)
    if num_events == 0:
        flash('There are no performances at this time.', 'warning')
        return redirect(url_for('index'))
    if 'event_id' in request.args:
        event_id = request.args.get('event_id')
        performance = Performances.query.get(event_id)
        performance_date = performance.date_of_performance.strftime('%Y-%m-%dT%H:%M')
        if request.method == "POST":
            if 'join_button' in request.form:
                if 'id' in session:
                    enter_event(current_user.id, performance.id, "Performances")
                    flash("You have successfully ticketed for the performance!", "success")
                else:
                    flash("You must be logged in to make this action!", "danger")

        return render_template('view_performance.html', event=performance, event_date=performance_date)

    events = Performances.query.all()
    return render_template('performances.html', events=events)

@app.route('/events/tournaments', methods=['GET', 'POST'])
def display_tournaments(): 
    tournaments = Tournaments.query.all() #filter(not_(ProjectWednesday.cycle_number)).all()
    num_events = len(tournaments)
    if num_events == 0:
        flash('There are no tournaments at this time.', 'warning')
        return redirect(url_for('index'))
    if 'event_id' in request.args:
        event_id = request.args.get('event_id')
        tournament = Tournaments.query.get(event_id)
        tournament_date = tournament.date_of_tournament.strftime('%Y-%m-%dT%H:%M')
        print(tournament)
        if not isinstance(tournament, Tournaments):
            flash('That event is not a tournament', 'danger')
            return redirect(url_for('event'))

        if request.method == "POST":
            if 'join_button_competitor' in request.form:
                if 'id' in session:
                    enter_event(current_user.id, tournament.id, "Tournaments Competing")
                    flash("You have successfully entered the tournament as a competitor!", "success")
                else:
                    flash("You must be logged in to make this action!", "danger")
            if 'join_button_spectator' in request.form:
                if 'id' in session:
                    enter_event(current_user.id, tournament.id, "Tournaments Spectating")
                    flash("You have successfully registered as a spectator for this tournament!", "success")
                else:
                    flash("You must be logged in to make this action!", "danger")
            if 'leave_event' in request.form:
                if 'id' in session:
                    if current_user.id in tournament.participants["Competitors"]:
                        leave_event(current_user.id, tournament.id, "Tournaments Competing")
                        flash("You have successfully registered left this tournament!", "success")
                    elif current_user.id in tournament.participants["Joined Users"]:
                        leave_event(current_user.id, tournament.id, "Tournaments Spectating")
                        flash("You have successfully registered left this tournament!", "success")
                    else:
                        flash("You have not joined this event", 'warning')
                else:
                    flash("You must be logged in to make this action!", "danger")
        if 'id' in session:
            return render_template('view_tournament.html', event=tournament, user = current_user, event_date = tournament_date)
        return render_template('view_tournament.html', event=tournament, user = '', event_date = tournament_date)

    events = Tournaments.query.all()
    return render_template('tournaments.html', events=events)

#  if request.method=='GET':
#         per_page = 5
#         page = request.args.get('page', 1, type=int)
#         offset = (page-1) * per_page
#         # items = get_items(offset)
          
#         pagination = Pagination(page=page, total=Book.query.count(), record_name='items',per_page=per_page)
#         books = Book.query.paginate(page=page,per_page=per_page)
#         return render_template("inventory.html", books = books, pagination=pagination)

@app.route("/add")
# @login_required
def add():
    return render_template("add_event_determination.html")

# @app.route("/add/performances", methods=['GET', 'POST'])
# # @login_required
# def add_performances():
#     if request.method == "POST":
#         name = request.form['event_title']
#         description = request.form['event_description']
#         date = request.form['date_of_torunament']
#         student_limit = request.form['student_limit']
#         if 'event_pic' not in request.files:
#             event_pic = ''
#         else:
#             event_pic = request.files['event_pic'] 
#         cost_audience = request.form['cost_audience']

#         new_performance = Performances(
#             creator_id = current_user.id,
#             name = name,
#             description = description,
#             student_limit = student_limit,
#             image = event_pic,
#             date_of_tournament = date,
#             cost_audience = cost_audience,
#         )
        
#         flash('Performance added successfully!', 'success')
        
#IMAGE PROCESSING WITH PERFORMANCE MUST BE DONE.


def process_tournament_data():
        name = request.form['event_title']
        description = request.form['event_description']
        datetime_data = request.form['date_of_tournament']
        date = datetime.strptime(datetime_data, '%Y-%m-%dT%H:%M')
        student_limit = request.form['student_limit']
        if 'event_pic' not in request.files:
            event_pic_data = ''
        else:
            event_pic_file = request.files['event_pic'] 
            event_pic_data = event_pic_file.read()
            image_data_b64 = base64.b64encode(event_pic_data).decode('utf-8')
        cost_competitor = request.form['cost_competitor']
        cost_spectator = request.form['cost_spectator']

        new_tournament = Tournaments(
            creator_id = current_user.id,
            name = name,
            description = description,
            student_limit = student_limit,
            image = event_pic_data,
            image_b64 = image_data_b64,
            date_of_tournament = date,
            cost_competitor = cost_competitor,
            cost_spectator = cost_spectator,
        )
        
        db.session.add(new_tournament)
        db.session.commit()
        
        flash('Tournament added successfully!', 'success')

def process_project_data():
        name = request.form['name']
        description = request.form['project_description']
        student_limit = request.form['student_limit']
        teachers = request.form['teachers']
        student_assistant = request.form['student_assistant']
        special_note = request.form['special_note']
        cycle_num = request.form['cycle']
        if request.form['cost'] != '':
            cost = request.form['cost']
        new_pw = ProjectWednesday(
            creator_id = current_user.id,
            name = name,
            description = description,
            student_limit = student_limit,
            cycle_number = cycle_num,
            teachers = teachers,
            student_assistant = student_assistant,
            special_note = special_note,
        )
        
        db.session.add(new_pw)
        db.session.commit()
        
        flash('Project added successfully!', 'success')

def process_performance_data():
        name = request.form['event_title']
        description = request.form['event_description']
        datetime_data = request.form['date_of_performance']
        date = datetime.strptime(datetime_data, '%Y-%m-%dT%H:%M')
        student_limit = request.form['student_limit']
        if 'event_pic' not in request.files:
            event_pic_data = ''
        else:
            event_pic_file = request.files['event_pic'] 
            event_pic_data = event_pic_file.read()
            image_data_b64 = base64.b64encode(event_pic_data).decode('utf-8')
        cost_audience = request.form['cost_audience']

        new_performance = Performances(
            creator_id = current_user.id,
            name = name,
            description = description,
            student_limit = student_limit,
            image = event_pic_data,
            image_b64 = image_data_b64,
            date_of_performance = date,
            cost_audience = cost_audience
        )
        
        db.session.add(new_performance)
        db.session.commit()
        
        flash('Performance added successfully!', 'success')


@app.route("/add/performances", methods=['GET', 'POST'])
# @login_required
def add_performance_route():
    return render_template("add-events-performance.html")

@app.route("/add/project_wednesdays", methods=['GET', 'POST'])
@login_required
def add_projects():
    if request.method == "POST":
        if 'event_submit' in request.form:
            name = request.form['name']
            description = request.form['project_description']
            student_limit = request.form['student_limit']
            teachers = request.form['teachers']
            student_assistant = request.form['student_assistant']
            special_note = request.form['special_note']
            cycle_number = request.form['cycle']

            new_project = ProjectWednesday(
                creator_id=current_user.id,
                name=name,
                description=description,
                student_limit=student_limit,
                teachers=teachers,
                student_assistant=student_assistant,
                special_note=special_note,
                cycle_number=cycle_number
            )

            db.session.add(new_project)
            db.session.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('add_projects'))
        
        elif 'cycle_submit' in request.form:
            cycle_number = request.form['cycle']
            csv_file = request.files['csv_file']
            
            csv_data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(csv_data)
            for row in csv_reader:
                new_project = ProjectWednesday(
                    creator_id=current_user.id,
                    name=row[0],
                    description=row[1],
                    student_limit=row[2],
                    teachers=row[3],
                    student_assistant=row[4],
                    special_note=row[5],
                    cycle_number=cycle_number
                )
                db.session.add(new_project)

            db.session.commit()
            flash('Project cycle uploaded successfully!', 'success')
            return redirect(url_for('add_projects'))

    return render_template("add-events-pw.html")




@app.route("/add/tournaments")
# @login_required
def add_tournaments():
    return render_template("add-events-tournaments.html")

@app.route("/edit")
# @login_required
def edit():
    events = Event.query.filter_by(creator_id=current_user.id)
    return render_template("edit_event.html", events=events)

@app.route('/edit/performance')
def edit_performance():
    pass

@app.route('/remove_event')
def remove_event():
    event_id = request.args.get('event_id')
    print(event_id)
    event = Event.query.get(int(event_id))
    print(event)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event removed successfully!', 'success')
    except:
        db.session.rollback()
        flash('There was an issue removing the event. Please try again.', 'warning')
    return redirect(url_for('index'))

@app.route('/verify_email')
def email_verification():
    pass

@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.get(int(session['id']))
    if request.method == 'GET':
        p_wed = Event.query.filter_by(name=user.joined_events.get("Project Wednesday")).first()
        tournaments_s = [tournament for tournament in Tournaments.query.all() if user.id in tournament.participants["Joined Users"]]
        tournaments_c = [tournament for tournament in Tournaments.query.all() if user.id in tournament.participants["Competitors"]]
        return render_template('profile.html', user=user, event=p_wed, tournaments_c=tournaments_c, tournaments_s=tournaments_s)
    
    if request.method == "POST":
        if 'profile_submit' in request.form:
            first_name = request.form.get('newfirstname')
            last_name = request.form.get('newlastname')
            email = request.form.get('newemail')
            
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            db.session.commit()
            flash("Profile Information Edited Successfully!", "success")
            return redirect(url_for('profile'))
        
        elif "password_submit" in request.form:
            new_password = request.form.get("newpass")
            old_password = request.form.get('oldpass')
            if user and user.check_password(old_password):
                user.set_password(new_password)
                db.session.commit()
                flash("Password Successfully Changed!", 'success')
                return redirect(url_for('profile'))
            else:
                flash('Incorrect Password!', 'danger')
                return redirect(url_for('profile'))



# edit / add / profile 

# Import necessary modules
@app.route('/promote', methods=['GET', 'POST'])
@login_required
def promote():
    current_user_obj = User.query.get(int(session['id']))  # Retrieve the current user by ID
    users = User.query.all() 
    # Access control based on account type
    # if current_user_obj.account_type == 'Admin':
    #     # Retrieve all users except SuperAdmins and other Admins
    #     users = User.query.filter(User.account_type != 'SuperAdmin', User.account_type != 'Admin').all()
    # elif current_user_obj.account_type == 'SuperAdmin':
    #     users = User.query.all()  # SuperAdmins can see all users
    # else:
    #     flash('Unauthorized Access!', 'danger')
    #     return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('promote.html', users=users)  # Pass users to the template

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('new_role')

        if user_id and new_role:
            user_to_promote = User.query.get(int(user_id))

            if user_to_promote:
                # Check if the promotion is allowed
                if (current_user_obj.account_type == 'Admin' and user_to_promote.account_type in ['Admin', 'SuperAdmin']):
                    flash("Admins can't modify Admins or SuperAdmins.", 'danger')
                elif (current_user_obj.account_type == 'SuperAdmin' and user_to_promote.account_type == 'SuperAdmin'):
                    flash("SuperAdmins can't modify SuperAdmins.", 'danger')
                else:
                    user_to_promote.account_type = new_role  # Assign the new role
                    db.session.commit()  # Save changes

                    flash(f"User {user_to_promote.email} promoted to {new_role}", 'success')
            else:
                flash("User not found", 'danger')
        else:
            flash("Invalid promotion request", 'danger')

        return redirect(url_for('promote'))




def promote_self_to_superadmin():
    email = "your_email@example.com"  # Replace with your email
    user = User.query.filter_by(email=email).first()  # Retrieve the user by email

    if user:
        # Promote the user through class inheritance
        if not isinstance(user, SuperAdmin):
            user_account_type = user.account_type

            if user_account_type == "Student":
                # Reassign user to Teacher first
                user = Teacher(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    password_hash=user.password_hash,
                    account_type="Teacher"
                )
                db.session.commit()  # Save changes

            if user_account_type in ["Teacher", "Admin"]:
                # Reassign user to SuperAdmin
                user = SuperAdmin(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    password_hash=user.password_hash,
                    account_type="SuperAdmin"
                )
                db.session.commit()  # Save changes

        print(f"User {email} promoted to SuperAdmin.")
    else:
        print(f"User with email {email} not found.")



@app.route('/admin/users')
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    p_wed = Event.query.filter_by(name=user.joined_events.get("Project Wednesday")).first()
    tournaments_s = [tournament for tournament in Tournaments.query.all() if user.id in tournament.participants["Joined Users"]]
    tournaments_c = [tournament for tournament in Tournaments.query.all() if user.id in tournament.participants["Competitors"]]
    return render_template('profile.html', user=user, event=p_wed, tournaments_c=tournaments_c, tournaments_s=tournaments_s)

        


                 






if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)