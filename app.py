# import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from script import program
from pathlib import Path
# create flask app which refrences app.py
app = Flask(__name__)
# app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# create database
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres'

# basedir = os.path.abspath(os.path.dirname(__file__))
# brython_js = os.path.join(basedir, 'static/js/brython.js')
# brython_stdlib_js = os.path.join(basedir, 'static/js/brython_stdlib.js')
  
# Design the database
class  BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id) 




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
 
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html', posts=all_posts)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST', 'DELETE'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "error editing post"
    elif request.method == 'DELETE':
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return "error deleting post"
    else:
        # post = BlogPost.query.get_or_404(id)
        return render_template('edit.html', post=post)
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
    return Path('static/js/brython.js').read_text(), "text/javascript"


@app.route('/static/js/brython_stdlib.js')
def brython_stdlib_js():
    return Path('static/js/brython_stdlib.js').read_text(), "text/javascript"

@app.route('/home/users/<string:name>/posts/<int:idx>')
#code that will be run when the route is called
def greetings(name, idx):
    return "hello, " + name + ". This is your " + str(idx) + " post"

@app.route('/onlyget', methods=['GET'])
def getrequest():
    return 'you can get this using get request'

# python best practices
if __name__ == '__main__':
    app.run(debug=True) 
