from flask import Flask, render_template

# create flask app
app = Flask(__name__)


all_posts =[
    {
    'title': 'Post 1',
    'content': 'This is the content of post 1'
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

@app.route('/posts')
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
