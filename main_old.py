from flask import Flask, render_template, request, redirect
import re
import os
import logging
from flask_sqlalchemy import SQLAlchemy

#from util import Config

from logging.config import dictConfig

db = SQLAlchemy()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

#config = Config.getConfig()

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/osa', methods=['GET'])
def osa():
    return render_template("osa.html")

@app.route('/gallery', methods=['GET'])
def gallery():
    return render_template("gallery.html")

@app.route('/schedule', methods=['GET'])
def schedule():
    return render_template("schedule.html")

@app.route('/faq', methods=['GET'])
def faq():
    return render_template("faq.html")

@app.route('/submit', methods=['POST'])
def submit():

    email = request.form["email"]
    jiraName = request.form["jname"]
    firstName = request.form["fname"]
    lastName = request.form["lname"]
    group = request.form["group"]
    
#    result, errMessage = provider.add_crowd_user(email, firstName, lastName, jiraName, group)

#    if (not result):
#        return render_template("error.html", errormsg=errMessage)
    
#    return render_template("success.html", email=email, jname=jiraName,fname=firstName, lname=lastName,group=group)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')