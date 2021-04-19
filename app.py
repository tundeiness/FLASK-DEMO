from __future__ import print_function # In python 2.7
import os
from flask import Flask,render_template, request, jsonify, url_for, redirect, session, g, flash, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from pathlib import Path
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import IntRangeType, create_database, database_exists
import sqlite3
import enum
from sqlite3 import Error
import json
# from flask_modus import Modus
from flask_bcrypt import Bcrypt
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, validators, SelectField, SubmitField
from sqlalchemy.exc import IntegrityError
from application.decorators import enforce_auth, prevent_login_signup, enforce_correct_user, check_admin
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from country import COUNTRY
from restrict import RESTRICTION_TYPE
import sys
from middleware import HTTPMethodOverrideMiddleware




# Initialise app
app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
app.secret_key = 'formyeyesonlysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__, template_folder="templates")

# Check environment

# ENV = 'dev'
# ENV = 'prod'

# if ENV == 'dev':
    # app.debug = True
    # create database with postgres 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postgres:12345@localhost/main' 
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///localhost/main' 
# else:
    # app.debug() = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = ''



# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tour.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




# SQlite configurations
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'database'
# app.config['MYSQL_HOST'] = 'localhost'
# mysql.init_app(app)


# username = 'sqlite'
# host = 'localhost'
# port = 5005
# DB_NAME = 'tour_db'

# Create database
# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# engine = create_engine(f"sqlite:///{username}:{password}@{host}:{port}")

# tour_db = 'sqlite:///{0}:{1}@{2}:{3}'.format(username, password, host, port)
# tour_db = 'sqlite:///{0}@{1}:{2}'.format(username, host, port)
# engine = "sqlite:///localhost/tour_db"
# engine = create_engine("sqlite:///localhost/tour_db")
# if not database_exists(tour_db):
#     create_database(tour_db)


# engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(basedir, 'db2.sqlite') 
# engine = create_engine('sqlite:///' + os.path.join(basedir, 'db2.sqlite'))
# conn = engine.connect()
# conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
# conn.close()

# modus = Modus(app)

bcrypt = Bcrypt(app)

# initialise database
db = SQLAlchemy(app)

# Initialise marshmallow
ma = Marshmallow(app)



class RestrictionType(enum.Enum):
    unknown = "unknown"
    required = "required"
    unrequired = "unrequired"


# TravelPermit Class/Model
class TravelPermit(db.Model):
    __tablename__ = 'travel_permit'
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    visa = db.Column(db.Enum(RestrictionType), nullable=False, default=RestrictionType.unknown.value)
    quarantine = db.Column(db.Enum(RestrictionType), nullable=False, default=RestrictionType.unknown.value)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # db.Column(db.Enum(RestrictionType))
    # value = db.Column(Enum(RestrictionType))

# constructor
def __init__(self, home, destination, visa=RestrictionType.unknown.name, quarantine=RestrictionType.unknown.value):
    self.home =  home
    self.destination = destination
    self.visa = visa
    self.quarantine = quarantine

def __repr__(self):
    return '<TravelPermit %r>' % self.location 


# TravelPermit Schema

class TravelPermitSchema(ma.Schema):
    class Meta:
        fields = ('id','home','destination','visa','quarantine')
        


# Initialise schema 
travel_permit_schema = TravelPermitSchema()
travel_permits_schema = TravelPermitSchema(many=True)




ACCESS = {
    'guest': 0,
    'user': 200,
    'admin': 300
}


# User Class/Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(128), nullable=True)
    access = db.Column(db.Integer, nullable=False, default=ACCESS['user'])
    reg_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
            return '<User {}>'.format(self.username)    

    # constructor
    def __init__(self,first_name, last_name, username, email, password, access=ACCESS['admin']):
        self.first_name=  first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.access = access
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

# def is_admin(self):
#         return self.access == ACCESS['admin']
    
# def allowed(self, access):
#         return self.access >= access




@classmethod
def authenticate(cls, email, password):
    user = cls.query.filter_by(email = email).first()
    if user:
        is_authenticated = bcrypt.check_password_hash(user.password, password)
        if is_authenticated:
            return user
    return False

def __repr__(self):
    return f'<User: {self.username}>' 



class UserSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email')


# Initialise schema 
user_schema = UserSchema()
users_schema = UserSchema(many=True)



class SignupForm(FlaskForm):
    first_name = StringField('First Name', [validators.InputRequired(), validators.Length(min=5, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=5, max=50)])
    username = StringField('Username', [validators.Length(min=5, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
    validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired(),
    validators.EqualTo('password', message='Password do not match')])
    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=50)])
    email = StringField("Email", validators=[validators.Length(min=6, max=50), 
    validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])
    remember = BooleanField('remember me')
    submit = SubmitField('Log in')
    # password = PasswordField('Password', [validators.DataRequired(),
    # validators.EqualTo('confirm', message='Password do not match')])




# class CountrySelectField(SelectField):
#     def __init__(self, *args, **kwargs):
#         super(CountrySelectField, self).__init__(*args, **kwargs)
#         self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

# class Country(db.Model):
#     __tablename__ = 'country'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)


# # constructor
# def __init__(self, name):
#     self.name = name



class CountryForm(FlaskForm):  
    country = SelectField(label='Country', choices=COUNTRY)
    submit = SubmitField("Submit")

# def country_query():
#     return Country.query

# class CountryForm(FlaskForm):
#     opts=QuerySelectField(query_factory=country_query, allow_blank=True, get_label='name')


# @app.route('/users', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')


class TravelPermitForm(FlaskForm):
    home = SelectField(label='Country From', choices=COUNTRY)
    destination = SelectField(label='Country To', choices=COUNTRY)
    visa = SelectField(label='Visa Requirement', choices=RESTRICTION_TYPE)
    quarantine = SelectField(label='Covid Testing', choices=RESTRICTION_TYPE)
    submit = SubmitField("Submit")



# @app.route('/users', methods=['POST'])
# def index():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('users/templates/index.html', users=User.query.all())

def get_details():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user


def query_users():
    users = User.query.all()
    return users


# @enforce_auth
# @app.route('/signup')
# def index():
#     return render_template('index.html', users=User.query.all())
#     pass



# def check_admin():
#     """
#     Prevent non-admins from accessing the page
#     """
#     if g.user.access < 300:
#         abort(403)


@app.route('/signup', methods=['GET','POST'])
@prevent_login_signup
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        try:
            new_user = User(first_name=first_name, last_name=last_name, username=username, email=email,access=300, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            flash('Sign up successful')
            return redirect(url_for('profile'))
        except IntegrityError:
            flash('Details already exists')
            return render_template('register.html')
    return render_template('register.html', form=form)



@app.before_request
def before_request():
    g.user = None 
    if 'email' in session:
        found_user = [x for x in query_users() if x.email == session['email']][0]
        g.user = found_user 


    #     session.pop('user_id', None)
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     found_user = [x for x in query_users() if x.username == username][0]
    #     if found_user and found_user.password == password:
    #         session['user_id'] = found_user.id
    #         return redirect(url_for('profile'))
    #     return redirect(url_for('login'))
    # return render_template('signup.html')
    # if request.method == 'POST':
    # return render_template('signup.html')
        # db.session.add(get_details())
        # db.session.commit()
        # return redirect(url_for('signup'))#redirect to users/login method
    # return render_template('signup.html')
    # return redirect(url_for('signup'))#redirect to users/login method
    # else:
        # return render_template('profile.html')
        # first_name = request.form.get('first_name')
        # last_name = request.form.get('last_name')
        # username = request.form.get('username')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # check_user = User.query.filter_by(email=email).first()
        # new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        # if check_user:
        #     # Flash message letting user know they need to login
        #     return redirect(url_for('login')) #redirect to users/login method
        # else:
        #     # new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        #     db.session.add(new_user)
        #     db.session.commit()
        # # need a flash message here
        # return render_template('users/templates/profile.html', user=new_user)


# @app.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = bcrypt.generate_password_hash(password).decode('UTF-8')
#         if username and email and password:
#             hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
#             check_user = User.query.filter_by(email=email).first()
#             if not check_user:
#                 new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 return redirect(url_for('login'))
#             else:
#                 return "A user with these details already exist"
#         else:
#             return "Fill the required fields"
#     else:
#      return render_template('register.html')     


    #     new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     flash('Sign up successful', 'success')
    #     return redirect(url_for('login'))
    # return render_template('register.html')


# USERS SIGNUP
# @app.route('/users/signup', methods=['GET','POST'])
# def signup():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         check_user = User.query.filter_by(email=email).first()
#         new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#         if check_user:
#             # Flash message letting user know they need to login
#             return redirect(url_for('login')) #redirect to users/login method
#         else:
#             # new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#             db.session.add(new_user)
#             db.session.commit()
#         # need a flash message here
#         return render_template('users/templates/profile.html', user=new_user)
    # return render_template('users/templates/index.html', users=User.query.all())


        # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        # if user: # if a user is found, we want to redirect back to signup page so user can try again
            # return redirect(url_for('auth.signup'))
            # return redirect('/signup')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        # db.session.add(new_user)
        # db.session.commit()

        # return redirect('/login')
        # return redirect(url_for('auth.login'))

        # self.first_name=  first_name
        # self.last_name = last_name
        # self.username = username
        # self.email = email
        # self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

# @app.before_request
# def before_request():
#     g.user = None 

#     if 'email' in session:
#         found_user = [x for x in query_users() if x.email == session['email']][0]
#         g.user = found_user 



# @app.before_request
# def current_user():
#     if session.get('email'):
#         g.current_user = User.query.get(session['email'])
#     else:
#         g.current_user = None



# USERS lOGIN
# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         session.pop('user_id', None)
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         found_user = [x for x in query_users() if x.username == username][0]
#         if found_user and found_user.password == password:
#             session['user_id'] = found_user.id
#             return redirect(url_for('profile'))
#         return redirect(url_for('login'))
#     return render_template('login.html')


# Admin gets redirected to a special Admin template when they log  in
# @app.route('/login', methods=['GET','POST'])
# @prevent_login_signup
# def login():
#     # Creating Login form object
#     form = LoginForm(request.form)
#     # verifying that method is post and form is valid
#     if request.method == 'POST':
#         # checking that user is exist or not by email
#         email = request.form.get('email')
#         password_candidate = request.form.get('password')
#         user = User.query.filter_by(email = form.email.data).first()
#         # authenticated_user = bcrypt.check_password_hash(user.password, form.password.data)
#         # is_user = bcrypt.check_password_hash(user.password, password_candidate)
#         print(user, flush=True)
#         if user:
#             # if user exist in database than we will compare our 
#             # database hashed password and password come from login form 
#             # authenticated_user = bcrypt.check_password_hash(user.password, form.password.data)
#             is_user = bcrypt.check_password_hash(user.password, password_candidate)
#             if is_user:
#                 flash('You have successfully logged in.')
#                 session['logged_in'] = True
#                 session['email'] = user.email 
#                 session['username'] = user.username
#                 # After successful login, redirecting to home page
#                 return redirect(url_for('profile'))
#                 if user.access >= 300:
#                     # if password is matched, allow user to access and 
#                     # save email and username inside the session 
#                     # return 'Logged in!!'
#                     # flash('You have successfully logged in.')
#                     # session['logged_in'] = True
#                     # session['email'] = user.email 
#                     # session['username'] = user.username
#                     # # After successful login, redirecting to home page
#                     # return redirect(url_for('profile'))
#                     flash('Welcome Admin.')
#                     session['logged_in'] = True
#                     session['email'] = user.email 
#                     session['username'] = user.username
#                     session['access'] = user.access
#                     return redirect(url_for('admin_dashboard'))
#                 else:
#                     # flash('Invalid email or password.')
#                     # return redirect(url_for('login'))
#                     return redirect(url_for('profile'))
#             # when login details are incorrect        
#         else:
#             flash('Invalid email or password.')
#     return render_template('login.html', form = form)
#         # if check_user:
#         #     return render_template('users/templates/profile.html', user=username)
#         # else:
#         #     # a Flash message will be adequate for this
#         #     return 'wrong email or password'

@app.route('/login', methods=['GET','POST'])
@prevent_login_signup
def login():
    # Creating Login form object
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == 'POST':
        # checking that user is exist or not by email
        email = request.form.get('email')
        password_candidate = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        print(email, flush=True)
        # is_user = bcrypt.check_password_hash(user.password, password_candidate)
        if user is not None and bcrypt.check_password_hash(user.password, password_candidate): 
            session['logged_in'] = True
            session['email'] = user.email 
            session['username'] = user.username
            session['access'] = user.access
            return redirect(url_for('profile'))
        else:
            flash('user not found')
            return render_template('login.html', form = form)
    return render_template('login.html', form = form)       


# USERS lOGOUT
@app.route('/logout')
def logout():
    # Removing data from session by setting logged_flag to False.
    session.pop('email', None)
    flash('Logged out!')
    # redirecting to home page
    return redirect(url_for('root'))




# @app.route('/logout', methods=['DELETE'])
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('/'))
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     users = User.query.all()
    #     # check_user = User.query.filter_by(email=email).first()
    #     # found_user = [user for  user in users if user.password == password][0]
    #     for user in users:
    #         if user.password == password:
    #             found_user = user
    #             return render_template('users/templates/profile.html', user=found_user)
    #         else:
    #             return 'wrong email or password'

        # if check_user:
        #     return render_template('users/templates/profile.html', user=username)
        # else:
        #     # a Flash message will be adequate for this
        #     return 'wrong email or password'



# GET ALL USERS
# get all users if user is Admin
@app.route('/users', methods=['GET'])
def alluser():
    all_user = User.query.all()
    # return render_template('users/templates/index.html', users=all_user)
    result = users_schema.dump(all_user)
    return jsonify(result)
    #return render_template('users/templates/signup.html')


def get_curr_user():
    if 'email' in session:
        found_user = [x for x in query_users() if x.email == session['email']][0]
        return found_user 



# def update_users():
#     if enforce_correct_user:
#         form = CountryForm(request.form)
#         first = request.form.get('country_select')
#         conn = sqlite3.connect('tour.db')
#         cur = conn.cursor()
#         email =  session.get('email')
#         cur.execute('''UPDATE users SET country = ? WHERE email = ?''', (first, get_curr_user().email))
#         conn.commit()
#         conn.close()

# class CountryForm(Form):
#     country = SelectField(label='Country', choice=COUNTRY)
# def data_entry():
#     if g.user:
#         form = CountryForm(request.form)
#         first = request.form.get('country_select')
#         conn = sqlite3.connect('tour.db') 
#         c = conn.cursor()
#         c.execute("INSERT INTO users (country) VALUES (?)",(first) )
#         conn.commit() 


# @event.listen(User.__table__, 'after_create',
#             DDL(""" INSERT INTO users (email, country) VALUES (1, 'low') """))



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = CountryForm(request.form)
    first = request.form.get('country_select')
    permits = TravelPermit.query.all()
    users = User.query.all()
    print(first, flush=True)
    if not g.user:
        return redirect(url_for('login'))
    else:
        print(g.user.id)
        cond = form.validate()
        print(cond, flush=True)
        if request.method == 'POST':
            # import IPython
            # IPython.embed(first)
            # c = User(country=first)
            # db.session.add(c)
            # db.session.commit()
            # db.session.execute('UPDATE users SET country = ? WHERE country = ?', (first, None))
            # db.commit()
            # try:
            #     with sqlite3.connect("tour.db") as con:
            #         cur = con.cursor()
            #         print("Opened database successfully")
            #         # cur.execute('''INSERT INTO users (email, country) VALUES (g.user.email, first) ''')
            #         # cur.execute("INSERT INTO users (country) VALUE (?)",(first) )
            #         cur.execute('''UPDATE users SET country = ? WHERE country = ?''', (first,""))
            #         con.commit()
            #     flash("Record successfully added")
            # except:
            #     con.rollback()
            #     flash("error in insert operation")
            # finally:
            new_rec = User.query.filter_by(email=g.user.email).first()
            new_rec.country = first
            db.session.commit()
            flash("Record successfully added")
            return render_template("profile.html", msg = first, form=form, country=first, user=get_curr_user())
            # con.close()
    return render_template('profile.html', user=users, form=form, country=first, permits=permits)


# @app.route('/admin', methods=['GET', 'POST'])
# @check_admin
# def admin_dashboard():
#     # check_admin()
#     users = User.query.all()
#     permits = TravelPermit.query.all()
#     return render_template("admin.html", all_users=users)






# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     form = CountryForm(request.form)
#     selected_country = request.form.get('country_select')
#     # print(selected_country, flush=True)
#     if not g.user:
#         return redirect(url_for('login'))
#     else:
#         print(g.user.id)
#         cond = form.validate()
#         print(cond, flush=True)
#         # user = User.find_by_email(session['email'])
#         user = User.query.get(session['email'])
#         if request.method == 'POST' and g.user.access > 200:
#             new_rec = User.query.filter_by(email=g.user.email).first()
#             new_rec.country = selected_country
#             db.session.commit()
#             flash("Record successfully added")
#             return render_template("dashboard.html", form=form, country=selected_country)
#         else:
#             new_rec = User.query.filter_by(email=g.user.email).first()
#             new_rec.country = selected_country
#             db.session.commit()
#             flash("Record successfully added")
#             return render_template("profile.html", msg = selected_country, form=form, country=selected_country)
#     return render_template('profile.html', user=get_curr_user(), form=form, country=selected_country)


    # user = User.find_by_email(session['email'])
    # if not user.is_admin():
    #     return redirect(url_for('login'))
    
    # return render_template('dashboard.html')


            # import IPython
            # IPython.embed(first)
            # c = User(country=first)
            # db.session.add(c)
            # db.session.commit()
            # db.session.execute('UPDATE users SET country = ? WHERE country = ?', (first, None))
            # db.commit()
            # try:
            #     with sqlite3.connect("tour.db") as con:
            #         cur = con.cursor()
            #         print("Opened database successfully")
            #         # cur.execute('''INSERT INTO users (email, country) VALUES (g.user.email, first) ''')
            #         # cur.execute("INSERT INTO users (country) VALUE (?)",(first) )
            #         cur.execute('''UPDATE users SET country = ? WHERE country = ?''', (first,""))
            #         con.commit()
            #     flash("Record successfully added")
            # except:
            #     con.rollback()
            #     flash("error in insert operation")
            # finally:
                

                # """
                #     UPDATE users
                #     SET country = res_str
                #     WHERE email = email;
                # """
    # return render_template('profile.html', user=get_curr_user(), form=form)


# @app.route('/admin')
# # @login_required
# def admin():
#     user = User.query.filter_by(email=g.user.email).first()
#     if user.access <= 200:
#         abort(403)
#     else:
#         users = User.query.order_by(User.id).all()
#         return render_template('admin_view_users.html', users=users)
#     return redirect(url_for('stocks.watch_list'))






# @app.route('/admin/dashboard')
# def admin_dashboard():
#     # prevent non-admins from accessing the page
#     if g.user.access < 300:
#         abort(403)

#     return render_template('admin_dashboard.html', title="Dashboard")


# @app.route('/admin', methods=['GET', 'POST'])
# @check_admin
# def admin_dashboard():
#     # check_admin()
#     users = User.query.all()
#     permits = TravelPermit.query.all()
#     return render_template("admin.html", all_users=users)
    # form = CountryForm(request.form)
    # selected_country = request.form.get('country_select')
    # if request.method == 'POST':
    #     new_rec = User.query.filter_by(email=g.user.email).first()
    #     new_rec.country = selected_country
    #     db.session.commit()
    #     flash("Record successfully added")
    #     return render_template("dashboard.html", form=form, country=selected_country)
    # else:
    #     new_rec = User.query.filter_by(email=g.user.email).first()
    #     new_rec.country = selected_country
    #     db.session.commit()
    #     flash("Record successfully added")
    #     return render_template("profile.html", msg = selected_country, form=form, country=selected_country)
    # return render_template('profile.html', user=get_curr_user(), form=form, country=selected_country)





# def admin_dashboard():
#     form = CountryForm(request.form)
#     selected_country = request.form.get('country_select')
#     # print(selected_country, flush=True)
#     if g.user.access < 300:
#         return redirect(url_for('profile'))
#     else:
#         if request.method == 'POST':
#             new_rec = User.query.filter_by(email=g.user.email).first()
#             new_rec.country = selected_country
#             db.session.commit()
#             flash("Record successfully added")
#             return render_template("dashboard.html", form=form, country=selected_country)
#         else:
#             new_rec = User.query.filter_by(email=g.user.email).first()
#             new_rec.country = selected_country
#             db.session.commit()
#             flash("Record successfully added")
#             return render_template("profile.html", msg = selected_country, form=form, country=selected_country)
#     return render_template('profile.html', user=get_curr_user(), form=form, country=selected_country)





# def create_admin():
#     admin_user = User(email= g.user.email, access=300)
#     db.session.add(admin_user)
#     db.session.commit()


# @app.route('/profile-submit', methods=['POST'])
# def submit():
#     form = CountryForm(request.form)
#     first = request.form.get('country_select')
#     sentence = 'you are in ' + first
#     if request.method == 'POST' and form.validate():
#         prev_session = session.get('country')
#         if prev_session is not None:
#             session['country'] = first
#             # save the value to users record
#             # commit database
#         select = request.form.get('country_select')
#         session['country'] = select
#         # data = (str(select))
#         return session.get('country')
#         # return data
#         # return render_template('main.html', form=form, data=first)
#         # print(session.get('country'))
#     return render_template('profile.html', form=form, select=sentence)
#     # return redirect(url_for('signup'))
#     # return Path('index.html').read_bytes();




# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres'

# basedir = os.path.abspath(os.path.dirname(__file__))
# brython_js = os.path.join(basedir, 'static/js/brython.js')
# brython_stdlib_js = os.path.join(basedir, 'static/js/brython_stdlib.js')
  
# Design the database
# BlogPost Class/Model
# class  BlogPost(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     author = db.Column(db.String(20), nullable=False, default='N/A')
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __repr__(self):
#         return 'Blog post ' + str(self.id) 

# @app.route('/submit', methods=['POST'])
# def submit():
#     form = CountryForm(request.form)
#     first = request.form.get('country_select')
#     sentence = 'you are in ' + first
#     if request.method == 'POST' and form.validate():
#         select = request.form.get('country_select')
#         session['country'] = select
#         # data = (str(select))
#         return session.get('country')
#         # return data
#         # return render_template('main.html', form=form, data=first)
#         # print(session.get('country'))
#     return render_template('main.html', form=form, select=sentence)
#     # return redirect(url_for('signup'))
#     # return Path('index.html').read_bytes();



# define route
@app.route('/', methods=['GET', 'POST'])
def root():
    form = CountryForm(request.form)
    first = request.form.get('country_select')
    sentence = 'you are in ' + str(first)
    res = make_response()
    if request.method == 'POST' and form.validate():
        select = request.form.get('country_select')
        session['country'] = select
        res.set_cookie('country', first)
        # nu_country = request.cookies.get('country')
        # data = (str(select))
        # first = session.get('country')
        # print(res.get_cookie('country'), flush=True)
        return session.get('country')
        # return data
        # return render_template('main.html', form=form, data=first)
        # print(session.get('country'))
    return render_template('main.html', form=form, select=sentence)


    # form = CountryForm(request.form)
    # first = request.form.get('country_select')
    # if request.method == 'POST' and form.validate():
    #     # selection = dict(form.country.choices).get(form.country.data)
    #     first = form.country.data
    #     select = request.form.get('value')
    #     # select = request.form['value']
    #     print(select) 
    #     session['country'] = select
    #     data = (str(select))
    #     # return data
    #     # return render_template('main.html', form=form, data=first)
    #     # print(session.get('country'))
    # return render_template('main.html', form=form, select=first)
    # # return redirect(url_for('signup'))
    # # return Path('index.html').read_bytes();


# Create a Permit

# @app.route('/travel-permit', methods=['POST'])
# def add_travel_permit():
#     # accessible to only the admin
#     check_admin()
#     form = TravelPermitForm(request.form)
#     if request.method == 'POST':
#         hoome = request.form.get('home_select')
#         destination = request.form.get('destination_select')
#         visa = request.form.get('visa_select')
#         quarantine = request.form.get('quarantine_select')
#         new_travel_permit = TravelPermit(home=hoome, destination=destination, visa=visa, quarantine=quarantine)
#         all_permits = TravelPermit.query.all()
#         db.session.add(new_travel_permit)
#         db.session.commit()
#         flash("New permit successfully added")
#         return render_template('admin.html', all_permits=all_permits)
#         # return travel_permit_schema.jsonify(new_travel_permit)
#     else:
#         return render_template('404.html')



# @app.route('/travel-permits', methods=["GET", "POST"])
# def permits():
#     check_admin()
#     if request.method == 'POST':
#         new_permit = TravelPermit(home=request.form.get('home_select'), destination=request.form.get('destination_select'), visa=request.form.get('visa_select'), quarantine=request.form.get('quarantine_select'))
#         db.session.add(new_permit)
#         db.session.commit()
#         redirect(url_for('permits'))
#     render_template('permits.html', permits=permits)


@app.route('/travel-permits', methods=["GET", "POST"])
def all_permits():
    home = request.form.get('home_select')
    if home is not None:
        conn = sqlite3.connect('tour.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
        result = cur.fetchall()
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    elif home is None:
        all_permits = TravelPermit.query.all()
        # conn = sqlite3.connect('tour.db')
        # cur = conn.cursor()
        # cur.execute("SELECT * FROM travel_permit")
        # result = cur.fetchall()
        # resp = jsonify(result)
        print(all_permits, flush=True)
        return render_template('all_permits.html', title='All Permits',user=get_curr_user(), permits=all_permits)
    else:
        return 'Not Found'
        conn.commit()
        conn.close()

# Get all permits
# @app.route('/travel-permit', methods=['GET'])
# def get_travel_permits():
#     # destination_query_params = request.args.get('destination')
#     # only admin can have access to all permits
#     home = request.args.get('home')
#     if home is not None:
#         conn = sqlite3.connect('tour.db')
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
#         result = cur.fetchall()
#         resp = jsonify(result)
#         resp.status_code = 200
#         return resp
#     elif home is None:
#         all_permits = TravelPermit.query.all()
#         result = travel_permits_schema.dump(all_permits)
#         return render_template('all_permits.html', permits=all_permits)
#         # return jsonify(result)
#     else:
#         # resp = jsonify('Traveller "home or destination" not found in query string')
#         # resp.status_code = 500
#         return 'Not Found'
#         conn.commit()
#         conn.close()






@app.route('/travel-permits/new', methods=["GET", "POST"])
@check_admin
def new_permit():
    check_admin()
    form = TravelPermitForm(request.form)
    all_permits = TravelPermit.query.all()
    if request.method == 'POST':
        hoome = request.form.get('home_select')
        destination = request.form.get('destination_select')
        visa = request.form.get('visa_select')
        quarantine = request.form.get('quarantine_select')
        print(visa, flush=True)
        new_travel_permit = TravelPermit(home=hoome, destination=destination, visa=visa, quarantine=quarantine)
        db.session.add(new_travel_permit)
        db.session.commit()
        flash("New permit successfully created and added")
        return redirect(url_for('profile'))
    return render_template('create_permit.html', title='New Permit', form=form)



#single permit
@app.route('/travel-permits/<int:permit_id>', methods=["GET", "POST"])
# a decorator to check if user is admin
def permit(permit_id):
    check_admin()
    permit = TravelPermit.query.get_or_404(permit_id)
    return render_template("permit.html",user=get_curr_user(), permit=permit)


#update permit
@app.route('/travel-permits/<int:permit_id>/update', methods=["GET", "POST"])
@check_admin
def update_permit(permit_id):
    # check_admin()
    permit = TravelPermit.query.get_or_404(permit_id)
    if g.user.access < 300:
        abort(403)
    form = TravelPermitForm(request.form)
    if request.method == 'POST':
        permit.home = request.form.get('home_select')
        permit.destination = request.form.get('destination_select')
        permit.visa = request.form.get('visa_select')
        permit.quarantine = request.form.get('quarantine_select')
        db.session.commit()
        flash('Permit updated')
        return redirect(url_for('permit', permit_id=permit.id))
    elif request.method == 'GET':
        # populate the dropdowns
        form.home.data = permit.home
        form.destination.data = permit.destination
        form.visa.data = permit.visa
        form.quarantine.data = permit.quarantine
    return render_template('create_permit.html', title='Update Permit', form=form)

# GET ALL PERMITS
# @app.route('/travel-permit', methods=['GET'])
# def get_permits():
#     permits = TravelPermit.query.all()
#     return render_template("permits.html", all_permits=permits)


# def find_permit(permit_id):
#     found_permit = [permit for permit in permits if permit.id == permit_id][0]
#     return found_permit
    # permit = TravelPermit.query.all()
    # return permit



# @app.route('/travel-permits/<int:id>', methods=["GET", "PATCH", "DELETE"])
# def show_permit(id):
#     found_permit = find_permit(id)
#     if request.method == b'PATCH':
#         found_permit.home = request.form.get('home_select')
#         found_permit.destination = request.form.get('destination_select')
#         found_permit.visa = request.form.get('visa_select')
#         found_permit.quarantine = request.form.get('quarantine_select')
#         return redirect(url_for('permits'))
#     if request.method == b'DELETE':
#         TravelPermit.remove(found_permit)
#         return redirect(url_for('permits'))
#     # found_permit = [permit for permit in permits if permit.id == id][0]
#     # for permit in permits:
#     #     if permit.id == id:
#     #         found_permit = permit
#     # travel_permit = TravelPermit.query.get_or_404(id)
#     return render_template('show_permit.html', permit=found_permit)


# @app.route('/travel-permits/<int:id>/edit')
# def edit_permit(id):
#     check_admin()
#     found_permit = find_permit(id)
#     return render_template('edit_permit.html', permit=found_permit)




# Get all permits
# @app.route('/travel-permit', methods=['GET'])
# def get_travel_permits():
#     # destination_query_params = request.args.get('destination')
#     # only admin can have access to all permits
#     home = request.args.get('home')
#     if home is not None:
#         conn = sqlite3.connect('tour.db')
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
#         result = cur.fetchall()
#         resp = jsonify(result)
#         resp.status_code = 200
#         return resp
#     elif home is None:
#         all_permits = TravelPermit.query.all()
#         result = travel_permits_schema.dump(all_permits)
#         return render_template('all_permits.html', permits=all_permits)
#         # return jsonify(result)
#     else:
#         # resp = jsonify('Traveller "home or destination" not found in query string')
#         # resp.status_code = 500
#         return 'Not Found'
#         conn.commit()
#         conn.close()



# @app.route('/travel_permit', methods=['GET'])
# def get_traveller_origin():
#         home = request.args.get('home')
#         destination = request.args.get('destination')
        # ex = TravelPermit.query.filter(TravelPermit.location == location)
        # print(ex)
        # if home:
        #     conn = sqlite3.connect('tour.db')
        #     cur = conn.cursor()
        #     cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
        #     result = cur.fetchall()
        #     resp = jsonify(result)
        #     resp.status_code = 200
        #     return resp
        # elif destination:
        #     conn = sqlite3.connect('tour.db')
        #     cur = conn.cursor()
        #     cur.execute("SELECT * FROM travel_permit WHERE destination=?", (destination,))
        #     result = cur.fetchall()
        #     resp = jsonify(result)
        #     resp.status_code = 200
        #     return resp
        # else:
        #     resp = jsonify('Traveller "home or destination" not found in query string')
        #     resp.status_code = 500
        #     return resp
        # conn.commit()
        # conn.close()





# Get Single permit

# @app.route('/travel-permit/<id_>', methods=['GET'])
# def get_travel_permit(id_):
#     travel_permit = TravelPermit.query.get_or_404(id_)
#     return travel_permit_schema.jsonify(travel_permit)


# Update a Permit

# @app.route('/travel-permit/<id_>', methods=['PUT'])
# def update_travel_permit(id_):
#     permit = TravelPermit.query.get_or_404(id_)
#     if request.method == 'PUT':
#         country_from = request.form.get('home_select')
#         country_to = request.form.get('destination_select')
#         visa = request.form.get('visa_select')
#         quarantine = request.form.get('quarantine_select')

#         permit.home = country_from
#         permit.destination = country_to
#         permit.visa = visa
#         permit.quarantine = quarantine

#         db.session.commit()
#         flash("Permit successfully edited")
#         all_permits = TravelPermit.query.all()
#         return render_template('permit-edit.html', permits=permit)
        # return travel_permit_schema.jsonify(permit)


# @app.route('/travel-permit/<id_>update', methods=['GET', 'POST'])
# # requires admin login
# def update_permit(id_):
#     permit = TravelPermit.query.get_or_404(id_)
#     if is_admin():
#         # do something
#         form = TravelPermitForm(request.form)
#         TravelPermit.home = request.form.get('home_select')
#         TravelPermit.destination = request.form.get('destination_select')
#         TravelPermit.visa = request.form.get('visa_select')
#         TravelPermit.quarantine = request.form.get('quarantine_select')
#         db.session.commit()
#         return render_template('index.html', title='update permit', legend='update permit')
#     else:
#         abort(403)


# Update a Permit

# @app.route('/travel-permit/<id_>', methods=['PUT'])
# def update_travel_permit(id_):
#     permit = TravelPermit.query.get_or_404(id_)
#     if request.method == 'PUT':
#         take_off_location = request.json['home']
#         travel_destination = request.json['destination']
#         visa = request.json['visa']
#         quarantine = request.json['quarantine']

#         permit.home = take_off_location
#         permit.destination = travel_destination
#         permit.visa = visa
#         permit.quarantine = quarantine

#         db.session.commit()
#         return travel_permit_schema.jsonify(permit)



# Get Delete permit

# @app.route('/travel-permit/<id_>', methods=['DELETE'])
# def delete_travel_permit(id_):
#     travel_permit = TravelPermit.query.get_or_404(id_)
#     db.session.delete(travel_permit)
#     db.session.commit()
#     return travel_permit_schema.jsonify(travel_permit)


# Get Query 
# @app.route('/travel_permit', methods=['GET'])
# def get_traveller_origin():
#         home = request.args.get('home')
#         destination = request.args.get('destination')
#         # ex = TravelPermit.query.filter(TravelPermit.location == location)
#         # print(ex)
#         if home:
#             conn = sqlite3.connect('tour.db')
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
#             result = cur.fetchall()
#             resp = jsonify(result)
#             resp.status_code = 200
#             return resp
#         elif destination:
#             conn = sqlite3.connect('tour.db')
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM travel_permit WHERE destination=?", (destination,))
#             result = cur.fetchall()
#             resp = jsonify(result)
#             resp.status_code = 200
#             return resp
#         else:
#             resp = jsonify('Traveller "home or destination" not found in query string')
#             resp.status_code = 500
#             return resp
#         conn.commit()
#         conn.close()



# CREATE TABLE IF NOT EXISTS projects (
# 	id integer PRIMARY KEY,
# 	name text NOT NULL,
# 	begin_date text,
# 	end_date text
# );

# create connection and create DB

def create_connection(tour_db):
    """ create a database connection to the SQLite database
        specified by tour_db
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect('tour.db')
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def main():
    # database = r"C:\sqlite\db\pythonsqlite.db"
    database = 'tour.db'

    sql_create_travel_permit_table = """ CREATE TABLE IF NOT EXISTS travel_permit (
                                        id integer PRIMARY KEY,
                                        home string NOT NULL,
                                        destination string NOT NULL,
                                        visa string NOT NULL,
                                        quarantine string NOT NULL,
                                        date_created text
                                    ); """

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        first_name string NOT NULL,
                                        last_name string NOT NULL,
                                        username string NOT NULL UNIQUE,
                                        email string NOT NULL,
                                        password text NOT NULL,
                                        country string,
                                        access integer NOT NULL,
                                        reg_date text
                                    ); """

    # sql_create_country_table = """ CREATE TABLE IF NOT EXISTS country (
    #                                     id integer PRIMARY KEY,
    #                                     name string NOT NULL,
    #                                 ); """

    # sql_create_traveller_table = """CREATE TABLE IF NOT EXISTS tasks (
    #                                 id integer PRIMARY KEY,
    #                                 name text NOT NULL,
    #                                 priority integer,
    #                                 status_id integer NOT NULL,
    #                                 project_id integer NOT NULL,
    #                                 begin_date text NOT NULL,
    #                                 end_date text NOT NULL,
    #                                 FOREIGN KEY (project_id) REFERENCES projects (id)
    #                             );"""
    




    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create travel_permit table
        create_table(conn, sql_create_travel_permit_table)
        # create users table
        create_table(conn, sql_create_users_table)

        # create country table
        # create_table(conn, sql_create_country_table)

        # create tasks table
        # create_table(conn, sql_create_traveller_table)
    else:
        print("Error! cannot create the database connection.")



# def populate_country():
#     conn = sqlite3.connect('tour.db')
#     cursor = conn.cursor()
#     # sqlstmt = """INSERT INTO country (name) VALUES (?)"""
#     # values = [(1,7,3000),(1,8,3500),(1,9,3900)]
#     listing = country.country
#     cursor.execute("INSERT INTO country (name) VALUES (?)", listing)


# User

# @app.route('/users', methods=["GET", "POST"])
# def index():
#     if request.method == 'POST':
#         first_name = request.json['first_name']
#         last_name = request.json['last_name']
#         username = request.json['username']
#         email = request.json['email']
#         password = request.json['password']
#         new_user = TravelPermit(home=take_off_location, destination=travel_destination, visa=visa, quarantine=quarantine)
#         db.session.add(new_user)
#         db.session.commit()
#         return user_schema.jsonify(new_user)




# @app.route('/signup', methods=['POST'])
# def signup_post():
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#         if user: # if a user is found, we want to redirect back to signup page so user can try again
#             # return redirect(url_for('auth.signup'))
#             return redirect('/signup')

#         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect('/login')
#         # return redirect(url_for('auth.login'))





# @app.route('/travel_permit', methods=['GET'])
# def get_traveller_destination():
#         destination = request.args.get('destination')
#         if destination:
#             conn = sqlite3.connect('db.sqlite')
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM travel_permit WHERE destination=?", (destination,))
#             result = cur.fetchall()
#             resp = jsonify(result)
#             resp.status_code = 200
#         else:
#             resp = jsonify('Traveller "destination" not found in query string')
#             resp.status_code = 500
#             return resp
#         conn.commit()
#         conn.close()

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

# # Get Query 
# @app.route('/travel_permit', methods=['GET'])
# def location_filter():
#     query_parameters = request.args

#     location = query_parameters.get('location')
#     destination = query_parameters.get('destination')

#     query = "SELECT * FROM TravelPermit WHERE"
#     to_filter = []

#     if location:
#         query += ' location=? AND'
#         to_filter.append(location)
#     if destination:
#         query += ' destination=? AND'
#         to_filter.append(destination)
#     if not (location or destination):
#         return 'page not found'

#     query = query[:-2] + ';'

#     conn = sqlite3.connect('db.sqlite')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()

#     results = cur.execute(query, to_filter).fetchall()

#     return jsonify(results)

    # return jsonify(location)
    # result = request.query_string
    # return jsonify(result)

# @app.route('/posts', methods=['GET', 'POST'])
# def posts():
#     if request.method == 'POST':
#         post_title = request.form['title']
#         post_content = request.form['content']
#         post_author = request.form['author']
#         new_post = BlogPost(title=post_title, content=post_content, author=post_author)
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect('/posts')
#     else:
#         all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
#         return render_template('post.html', posts=all_posts)


# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST', 'DELETE'])
# def edit(id):
#     post = BlogPost.query.get_or_404(id)

#     if request.method == 'POST':
#         post_title = request.form['title']
#         post_content = request.form['content']
#         post_author = request.form['author']

#         try:
#             db.session.commit()
#             return redirect('/posts')
#         except:
#             return "error editing post"
#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(post)
#             db.session.commit()
#             return redirect('/posts')
#         except:
#             return "error deleting post"
#     else:
#         return render_template('edit.html', post=post)
# def delete(id):
#     post = BlogPost.query.get_or_404(id)
#     if request.method == 'DELETE':
#         try:
#             db.session.delete(post)
#             db.session.commit()
#             return redirect('/posts')
#         except:
#             return "error deleting post"


# @app.route('/posts/delete/<int:id>')
# def delete(id):
#     post = BlogPost.query.get_or_404(id)
#     try:
#         db.session.delete(post)
#         db.session.commit()
#         return redirect('/posts')
#     except:
#         return "error deleting post"

 
@app.route('/static/js/brython.js')
def brython_js():
    return Path('static/js/brython.js').read_text(), 200, [("Content-Type", "text/javascript")]
    # return Path('static/js/brython.js').read_text(), "text/javascript"


@app.route('/static/js/brython_stdlib.js')
def brython_stdlib_js():
    return Path('static/js/brython_stdlib.js').read_text(), 200, [("Content-Type", "text/javascript")]
    # return Path('static/js/brython_stdlib.js').read_text(), "text/javascript"

@app.route('/static/img/vector-world-map.svg')
def world_map():
    return Path('static/img/vector-world-map.svg').read_text(), 200, [("Content-Type", 'image/svg+xml')]
    # return Path('static/img/vector-world-map.svg', mimetype='image/svg')
    

@app.route('/home/users/<string:name>/posts/<int:idx>')
#code that will be run when the route is called
def greetings(name, idx):
    return "hello, " + name + ". This is your " + str(idx) + " post"

@app.route('/onlyget', methods=['GET'])
def getrequest():
    return 'you can get this using get request'

# Run Server
if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0',port=5005, debug=True)
     
