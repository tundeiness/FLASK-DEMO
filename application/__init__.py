# from flask_bcrypt import Bcrypt
# import os
# from flask import Flask,render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from datetime import datetime
# from pathlib import Path
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy_utils import IntRangeType, create_database, database_exists
# import sqlite3
# from enum import Enum
# from sqlite3 import Error
# import json
# # from flask_modus import Modus



# # Initialise app
# app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# # app = Flask(__name__, template_folder="templates")

# # Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tour.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# # initialise database
# db = SQLAlchemy(app)

# # Initialise marshmallow
# ma = Marshmallow(app)


# # define route
# @app.route('/')
# def index():
#     return render_template('main.html')
#     # return Path('index.html').read_bytes();


# # Create a Permit

# @app.route('/travel-permit', methods=['POST'])
# def add_travel_permit():
#     if request.method == 'POST':
#         take_off_location = request.json['home']
#         travel_destination = request.json['destination']
#         visa = request.json['visa']
#         quarantine = request.json['quarantine']
#         new_travel_permit = TravelPermit(home=take_off_location, destination=travel_destination, visa=visa, quarantine=quarantine)
#         db.session.add(new_travel_permit)
#         db.session.commit()
#         return travel_permit_schema.jsonify(new_travel_permit)

# # Get all permits

# @app.route('/travel-permit', methods=['GET'])
# def get_travel_permits():
#     home = request.args.get('home')
#     # destination_query_params = request.args.get('destination')
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
#         return jsonify(result)
#     else:
#         # resp = jsonify('Traveller "home or destination" not found in query string')
#         # resp.status_code = 500
#         return 'Not Found'
#         conn.commit()
#         conn.close()


# # Get Single permit

# @app.route('/travel-permit/<id_>', methods=['GET'])
# def get_travel_permit(id_):
#     travel_permit = TravelPermit.query.get_or_404(id_)
#     return travel_permit_schema.jsonify(travel_permit)


# # Update a Permit

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



# # Get Delete permit

# @app.route('/travel-permit/<id_>', methods=['DELETE'])
# def delete_travel_permit(id_):
#     travel_permit = TravelPermit.query.get_or_404(id_)
#     db.session.delete(travel_permit)
#     db.session.commit()
#     return travel_permit_schema.jsonify(travel_permit)



# def create_connection(tour_db):
#     """ create a database connection to the SQLite database
#         specified by tour_db
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect('tour.db')
#         return conn
#     except Error as e:
#         print(e)

#     return conn


# def create_table(conn, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)




# def main():
#     # database = r"C:\sqlite\db\pythonsqlite.db"
#     database = 'tour.db'

#     sql_create_travel_permit_table = """ CREATE TABLE IF NOT EXISTS travel_permit (
#                                         id integer PRIMARY KEY,
#                                         home string NOT NULL,
#                                         destination string NOT NULL,
#                                         visa string NOT NULL,
#                                         quarantine string NOT NULL,
#                                         date_created text
#                                     ); """

#     # sql_create_traveller_table = """CREATE TABLE IF NOT EXISTS tasks (
#     #                                 id integer PRIMARY KEY,
#     #                                 name text NOT NULL,
#     #                                 priority integer,
#     #                                 status_id integer NOT NULL,
#     #                                 project_id integer NOT NULL,
#     #                                 begin_date text NOT NULL,
#     #                                 end_date text NOT NULL,
#     #                                 FOREIGN KEY (project_id) REFERENCES projects (id)
#     #                             );"""


#     # create a database connection
#     conn = create_connection(database)

#     # create tables
#     if conn is not None:
#         # create travel_permit table
#         create_table(conn, sql_create_travel_permit_table)

#         # create tasks table
#         # create_table(conn, sql_create_traveller_table)
#     else:
#         print("Error! cannot create the database connection.")



# @app.route('/static/js/brython.js')
# def brython_js():
#     return Path('static/js/brython.js').read_text(), 200, [("Content-Type", "text/javascript")]
#     # return Path('static/js/brython.js').read_text(), "text/javascript"


# @app.route('/static/js/brython_stdlib.js')
# def brython_stdlib_js():
#     return Path('static/js/brython_stdlib.js').read_text(), 200, [("Content-Type", "text/javascript")]
#     # return Path('static/js/brython_stdlib.js').read_text(), "text/javascript"

# @app.route('/static/img/vector-world-map.svg')
# def world_map():
#     return Path('static/img/vector-world-map.svg').read_text(), 200, [("Content-Type", 'image/svg+xml')]
#     # return Path('static/img/vector-world-map.svg', mimetype='image/svg')
    

# @app.route('/home/users/<string:name>/posts/<int:idx>')
# #code that will be run when the route is called
# def greetings(name, idx):
#     return "hello, " + name + ". This is your " + str(idx) + " post"

# @app.route('/onlyget', methods=['GET'])
# def getrequest():
#     return 'you can get this using get request'