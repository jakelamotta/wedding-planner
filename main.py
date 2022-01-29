from flask import Blueprint,render_template, request, redirect, flash, current_app, url_for
from wedding import db, babel, app, login_manager, EmailHelper
from flask_login import login_required, current_user
from models import User, Guest
from auth import auth as auth_blueprint
from flask_babel import gettext, ngettext
import re

main = Blueprint('main', __name__)
whitelistName = "^[ÅåÄäÖöa-zA-Z\.\-, ]+$"
whitelistEmail = "^[ÅåÄäÖöa-zA-Z0-9@\.]+$"

@main.route('/')
@login_required
def index():
    return render_template("index.html", name=current_user.name, guests=getFormattedGuests(current_user))

@main.route('/osa', methods=['GET'])
@login_required
def osa():
    return render_template("osa.html", user=current_user, guests=getGuests(current_user))

@main.route('/our_story', methods=['GET'])
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
    return render_template("responses.html", guests=getAllGuests())

@main.route('/faq', methods=['GET'])
@login_required
def faq():
    return render_template("faq.html")

@main.route('/submit_osa', methods=['POST'])
@login_required
def submit_osa():
    guests = getGuests(current_user)
    name = request.form.get('guest_name')
    allGuestsRsvped = True
    for guest in guests:
        if guest.name == name:
            guest.isAttending = request.form.get('attending_' + guest.name) != None
            guest.nonAlcoholic = request.form.get('nonAlco_' + guest.name) != None

            food = request.form.get('food_' + guest.name)
            song = request.form.get('song_' + guest.name)

            if food == "" or re.match(whitelistName,food):
                guest.foodPreferences = request.form.get('food_' + guest.name)
            elif song == "" or re.match(whitelistName,song):
                guest.song = request.form.get('song_' + guest.name)
            else:
                error = "Disallowed characters used in form"
                return render_template("osa.html", user=current_user, guests=guests, error=error)
            guest.hasResponded = True
            db.session.add(guest)
        allGuestsRsvped = allGuestsRsvped and guest.hasResponded

    db.session.add(current_user)
    db.session.commit()

    flash('Response successfully updated')
    app.logger.info('Updated response for guest %s', name)

    if allGuestsRsvped:
        result = sendEmail(current_user.email, getFormattedGuests(current_user), guests)
        if not result:
            error = "Could not send email, something went wrong"
            return render_template("osa.html", user=current_user, guests=guests, error=error)
        flash('Email confirmation sent')

    return redirect(url_for("main.osa"))

@main.route('/save_email', methods=['POST'])
@login_required
def save_email():
    current_user.email = request.form.get('email')
    guests = getGuests(current_user)
    db.session.add(current_user)
    db.session.commit()
    flash('Email saved successfully')
    return render_template("osa.html", user=current_user, guests=guests)

def getGuests(current_user):
    guests = Guest.query.filter_by(userId=current_user.id).all()
    return guests

def getAllGuests():
    guests = Guest.query.all()
    return guests

def getFormattedGuests(current_user):
    guests = getGuests(current_user)

    if (len(guests) == 1):
        return guests[0].name
    elif (len(guests) > 1):
        first = True
        formattedString=""
        for guest in guests:
            if first:
                formattedString = guest.name
                first = False
            else:
                formattedString = formattedString + " & " + guest.name
        return formattedString
    else:
        return current_user.username

def sendEmail(recipient, name, guests):
    message = createConfirmationMessage(recipient, name, guests)
    app.logger.info('Sending email to %s', recipient)
    helper = EmailHelper()
    return helper.sendEmail(recipient, message)

def getGuestListForEmail(guest):
    attendString = "No"
    alcoholString = "Yes"
    songString = ""
    foodString = ""
    if guest.isAttending:
        attendString = "Yes"
    if guest.nonAlcoholic:
        alcoholString = "No"
    if guest.song != None:
        songString = guest.song
    if guest.foodPreferences != None:
        foodString = guest.foodPreferences

    formattedGuest = """

    Name: """ + guest.name + """
    Is attending: """ + attendString  + """
    Alcohol: """ + alcoholString  + """
    Song suggested for the party: """ + songString  + """
    Possible food preferences: """ + foodString

    return formattedGuest


def createConfirmationMessage(recipient, name, guests):
    initPart = """From: Vera & Kristian <no-reply@banaj-johansson.se>
To: To Person <""" + recipient + """>
Subject: Wedding of Vera and Kristian

    Hello """ + name + """,

    Your response have been updated, please verify that the information is correct and also remember to RSVP for each guest."""

    guestList = ""
    for guest in guests:
        guestList = guestList + getGuestListForEmail(guest)

    endPart = """

    There will be more information to come on the website so please keep yourself updated.

    We hope to see YOU on the weekend of the 11th of June.

    Love,
    Vera & Kristian
    """

    return initPart + guestList + endPart

# add to you main app code
@babel.localeselector
def get_locale():
    return 'se'

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

app.register_blueprint(main)
app.register_blueprint(auth_blueprint)
