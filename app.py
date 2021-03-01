from flask import Flask

# create flask app
app = Flask(__name__)

# define route
@app.route('/')
def index():
    return '''
    <h1>Home Page</h1>
    <p>Welcome Home</p>
    '''

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
