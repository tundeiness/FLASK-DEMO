from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres'


class  BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id) 




all_posts =[
    {
    'title': 'Post 1',
    'content': 'This is the content of post 1',
    'author':'Tunde'
    },
    {
    'title': 'Post 2',
    'content': 'This is the content of post too'
    }
]

# define route
@app.route('/')
def index():
    return render_template('main.html')
    # return Path('index.html').read_bytes();
 
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    return render_template('post.html', posts=all_posts)

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
