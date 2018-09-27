from werkzeug.security import *
from app import *
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "UserInfo"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ImageContents(db.Model):
    __tablename__ = "ImageInfo"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    name = db.Column(db.String(256), unique=True)
    path = db.Column(db.String(256), unique=True)
    thumbnail_path = db.Column(db.String(256), unique=True)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
