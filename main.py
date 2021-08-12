from flask import Blueprint,render_template, request, redirect, flash
from . import db
from flask_login import login_required, current_user
from .models import User, Guest

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template("index.html", name=current_user.name)

@main.route('/osa', methods=['GET'])
@login_required
def osa():
    return render_template("osa.html", user=current_user, guests=getGuests(current_user))

@main.route('/gallery', methods=['GET'])
@login_required
def gallery():
    return render_template("gallery.html")

@main.route('/schedule', methods=['GET'])
@login_required
def schedule():
    return render_template("schedule.html")

@main.route('/faq', methods=['GET'])
@login_required
def faq():
    return render_template("faq.html")

@main.route('/submit_osa', methods=['POST'])
@login_required
def submit_osa():
    current_user.email = request.form.get('email')
    current_user.song = request.form.get('song')
    guests = getGuests(current_user)

    for guest in guests:
        guest.isAttending = request.form.get('attending_' + guest.name) != None
        guest.nonAlcoholic = request.form.get('nonAlco_' + guest.name) != None
        guest.foodPreferences = request.form.get('food_' + guest.name)
        guest.hasResponded = True
        db.session.add(guest)


    db.session.add(current_user)
    db.session.commit()

    flash('Response successfully submitted')
    return render_template("osa.html", user=current_user, guests=guests)

def getGuests(current_user):
    guests = Guest.query.filter_by(userId=current_user.id).all()
    print("HEEEEEEEEEEEEJ")
    print(current_user.id)
    return guests