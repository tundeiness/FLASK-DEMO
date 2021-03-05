import os
from flask import Flask,render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from pathlib import Path
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import IntRangeType, create_database, database_exists
import sqlite3
from enum import Enum
from sqlite3 import Error
import json



# Initialise app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__, template_folder="templates")

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

# initialise database
db = SQLAlchemy(app)

# Initialise marshmallow
ma = Marshmallow(app)



class RestrictionType(str,Enum):
    unknown = "unknown"
    required = "required"
    unrequired = "unrequired"


# TravelPermit Class/Model
class TravelPermit(db.Model):
    __tablename__ = 'travel_permit'
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    visa = db.Column(db.Enum(RestrictionType), nullable=False, default=RestrictionType.unknown)
    quarantine = db.Column(db.Enum(RestrictionType), nullable=False, default=RestrictionType.unknown)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # db.Column(db.Enum(RestrictionType))
    # value = db.Column(Enum(RestrictionType))

# constructor
def __init__(self, home, destination, visa, quarantine):
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


# define route
@app.route('/')
def index():
    return render_template('main.html')
    # return Path('index.html').read_bytes();


# Create a Permit

@app.route('/travel-permit', methods=['POST'])
def add_travel_permit():
    if request.method == 'POST':
        take_off_location = request.json['home']
        travel_destination = request.json['destination']
        visa = request.json['visa']
        quarantine = request.json['quarantine']
        new_travel_permit = TravelPermit(home=take_off_location, destination=travel_destination, visa=visa, quarantine=quarantine)
        db.session.add(new_travel_permit)
        db.session.commit()
        return travel_permit_schema.jsonify(new_travel_permit)

# Get all permits

@app.route('/travel-permit', methods=['GET'])
def get_travel_permits():
    all_permits = TravelPermit.query.all()
    result = travel_permits_schema.dump(all_permits)
    return jsonify(result)




# Get Single permit

@app.route('/travel-permit/<id_>', methods=['GET'])
def get_travel_permit(id_):
    travel_permit = TravelPermit.query.get_or_404(id_)
    return travel_permit_schema.jsonify(travel_permit)


# Update a Permit

@app.route('/travel-permit/<id_>', methods=['PUT'])
def update_travel_permit(id_):
    permit = TravelPermit.query.get_or_404(id_)
    if request.method == 'PUT':
        take_off_location = request.json['home']
        travel_destination = request.json['destination']
        visa = request.json['visa']
        quarantine = request.json['quarantine']

        permit.home = take_off_location
        permit.destination = travel_destination
        permit.visa = visa
        permit.quarantine = quarantine

        db.session.commit()
        return travel_permit_schema.jsonify(permit)



# Get Delete permit

@app.route('/travel-permit/<id_>', methods=['DELETE'])
def delete_travel_permit(id_):
    travel_permit = TravelPermit.query.get_or_404(id_)
    db.session.delete(travel_permit)
    db.session.commit()
    return travel_permit_schema.jsonify(travel_permit)


# Get Query 
@app.route('/travel_permit', methods=['GET'])
def get_traveller_origin():
        home = request.args.get('home')
        destination = request.args.get('destination')
        # ex = TravelPermit.query.filter(TravelPermit.location == location)
        # print(ex)
        if home:
            conn = sqlite3.connect('tour.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM travel_permit WHERE home=?", (home,))
            result = cur.fetchall()
            resp = jsonify(result)
            resp.status_code = 200
            return resp
        elif destination:
            conn = sqlite3.connect('tour.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM travel_permit WHERE destination=?", (destination,))
            result = cur.fetchall()
            resp = jsonify(result)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('Traveller "home or destination" not found in query string')
            resp.status_code = 500
            return resp
        conn.commit()
        conn.close()



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

        # create tasks table
        # create_table(conn, sql_create_traveller_table)
    else:
        print("Error! cannot create the database connection.")


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
     
