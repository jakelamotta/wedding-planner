from flask import Blueprint,render_template, request, redirect, flash, current_app
from wedding import db, babel, app, login_manager
from flask_login import login_required, current_user
from models import User, Guest
from auth import auth as auth_blueprint
from flask_babel import gettext, ngettext

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template("index.html", name=current_user.name, guests=getFormattedGuests(current_user))

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

@main.route('/responses', methods=['GET'])
@login_required
def responses():
    return render_template("responses.html")

@main.route('/faq', methods=['GET'])
@login_required
def faq():
    return render_template("faq.html")

@main.route('/submit_osa', methods=['POST'])
@login_required
def submit_osa():
    current_user.email = request.form.get('email')
    guests = getGuests(current_user)

    for guest in guests:
        guest.isAttending = request.form.get('attending_' + guest.name) != None
        guest.nonAlcoholic = request.form.get('nonAlco_' + guest.name) != None
        guest.foodPreferences = request.form.get('food_' + guest.name)
        guest.song = request.form.get('song_' + guest.name)
        guest.hasResponded = True
        db.session.add(guest)


    db.session.add(current_user)
    db.session.commit()

    flash('Response successfully submitted')
    return render_template("osa.html", user=current_user, guests=guests)

def getGuests(current_user):
    guests = Guest.query.filter_by(userId=current_user.id).all()
    return guests

def getFormattedGuests(current_user):
    if (current_user.name == "admin"):
        return "admin"

    guests = getGuests(current_user)

    if (len(guests) == 1):
        return guests[0].name
    elif (len(guests) == 2):
        return guests[0].name + " and " + guests[1].name
    else:
        return guests[0].name + ", " + guests[1].name + " and " + guests[2].name


# add to you main app code
@babel.localeselector
def get_locale():
    print(request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()))
    return 'se'

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

app.register_blueprint(main)
app.register_blueprint(auth_blueprint)
