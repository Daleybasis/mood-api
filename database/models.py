from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class MoodSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now().date(), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    moods = db.relationship('MoodSubmission', backref='author', lazy='dynamic')

    def hashPassword(self):
        self.password = generate_password_hash(self.password).decode('utf8')


    def evalPassword(self, password):
        return check_password_hash(self.password, password)