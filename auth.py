from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Guest
from . import db
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)
#new_user = User(username="admin", password=generate_password_hash("olof och hasse ar vara grannar", method='sha256'), name="admin")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
@login_required
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
@login_required
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('fullname')
    guest1 = request.form.get('guest1')
    guest2 = request.form.get('guest2')
    guest3= request.form.get('guest3')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256:1000000'), name=name)

    # add the new user to the database
    db.session.add(new_user)

    dbGuest = Guest(name=name, userId=new_user.id)
    db.session.add(dbGuest)
    if (guest2 != None and guest2 != ""):
        dbGuest = Guest(name=guest2, userId=new_user.id)
        db.session.add(dbGuest)

    if (guest3 != None and guest3 != ""):
        dbGuest = Guest(name=guest3, userId=new_user.id)
        db.session.add(dbGuest)

    db.session.commit()

    flash('User successfully created')
    return redirect(url_for('auth.signup'))