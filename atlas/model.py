from flask_login import UserMixin
from atlas import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    qs = db.relationship('Question', backref='qs', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Question(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_question = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary, nullable=True)
    file_name = db.Column(db.String(380), nullable=True)
    content = db.Column(db.Text(4294000000))

    def __init__(self, content, person_id, file, file_name):
        self.content = content
        self.person_id = person_id
        self.file = file
        self.file_name = file_name
