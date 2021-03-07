from application import db, bcrypt
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self,first_name, last_name, username, email, password):
        self.first_name=  first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')