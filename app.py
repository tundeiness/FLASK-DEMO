import os
from flask import Flask,render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from pathlib import Path
from sqlalchemy_utils import IntRangeType


# Initialise app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__, template_folder="templates")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy(app)

# Initialise marshmallow
ma = Marshmallow(app)

# TravelPermit Class/Model
class TravelPermit(db.Model):
    # __tablename__ = 'travelpermits'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    visa = db.Column(db.Integer, IntRangeType(step=2), nullable=False, default=0)
    quarantine = db.Column(db.Integer, IntRangeType(step=2), nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# constructor
def __init__(self, location, destination, visa, quarantine):
    self.location =  location
    self.destination = destination
    self.visa = visa
    self.quarantine = quarantine

def __repr__(self):
    return '<TravelPermit %r>' % self.location 


# TravelPermit Schema

class TravelPermitSchema(ma.Schema):
    class Meta:
        fields = ('id','location','destination','visa','quarantine')
        


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




# all_posts =[
#     {
#     'title': 'Post 1',
#     'content': 'This is the content of post 1',
#     'author':'Tunde'
#     },
#     {
#     'title': 'Post 2',
#     'content': 'This is the content of post too'
#     }
# ]

# define route
@app.route('/')
def index():
    return render_template('main.html')
    # return Path('index.html').read_bytes();


# Create a Permit

@app.route('/travel-permit', methods=['POST'])
def add_travel_permit():
    if request.method == 'POST':
        take_off_location = request.json['location']
        travel_destination = request.json['destination']
        visa = request.json['visa']
        quarantine = request.json['quarantine']
        new_travel_permit = TravelPermit(location=take_off_location, destination=travel_destination, visa=visa, quarantine=quarantine )
        db.session.add(new_travel_permit)
        db.session.commit()
        return travel_permit_schema.jsonify(new_travel_permit)

# Get all permits

@app.route('/travel-permit', methods=['GET'])
def get_travel_permit():
    all_permits = TravelPermit.query.all()
    result = travel_permits_schema.dump(all_permits)
    return jsonify(result.data)


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
    app.run(debug=True) 
