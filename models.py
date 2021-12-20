from wedding import db, app, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))
    db.relationship('Guest', backref='user', lazy=True)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isAttending = db.Column(db.Boolean)
    hasResponded = db.Column(db.Boolean)
    song = db.Column(db.String(1000))
    foodPreferences = db.Column(db.String(1000))
    nonAlcoholic = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))