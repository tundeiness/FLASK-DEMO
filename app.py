from flask import Flask, render_template

# create flask app
app = Flask(__name__)

# define route
@app.route('/')
def index():
    return render_template('main.html')
    # return Path('index.html').read_bytes();

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
