import json
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from oauthlib.oauth2 import WebApplicationClient import requests


from database_setup import Base, Event


# # Configuration
# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
# GOOGLE_DISCOVERY_URL = (
#     "https://accounts.google.com/.well-known/openid-configuration"
# )

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('postgresql://postgres:1234@localhost/events')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Show all events
@app.route("/")
@app.route("/event")
def showEvent():
    events = session.query(Event).order_by(desc(Event.date))
    return render_template('events.html', events = events)


#Create a new event
@app.route("/event/new", methods=['GET', 'POST'])
def newEvent():
    if request.method == 'POST':
        newEvent = Event(name = request.form['name'], date = request.form['date'], time = request.form['time'],
            price = request.form['price'], venue = request.form['venue'], description = request.form['description'])
        session.add(newEvent)
        session.commit()
        return redirect(url_for('showEvent'))
    else:
        return render_template('newEvent.html')


#Edit an event
@app.route("/event/<int:event_id>/edit", methods = ['GET','POST'])
def editEvent(event_id):
    editedEvent = session.query(Event).filter_by(id = event_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedEvent.name = request.form['name']
            return redirect(url_for('showEvent'))
    else:
        return render_template('editEvent.html', event = editedEvent)


#Delete an event
@app.route("/event/<int:event_id>/delete", methods = ['GET','POST'])
def deleteEvent(event_id):
    eventToDelete = session.query(Event).filter_by(id = event_id).one()
    if request.method == 'POST':
        session.delete(eventToDelete)
        session.commit()
        return redirect(url_for('showEvent', event_id = event_id))
    else:
        return render_template('deleteEvent.html',event = eventToDelete)

#Show the information of an event
@app.route("/event/<int:event_id>/")
@app.route("/event/<int:event_id>/info")
def showEventInfo(event_id):
    event = session.query(Event).filter_by(id = event_id).one()
    return render_template('eventInfo.html', event = event)

#Edit the information of an event
@app.route("/event/<int:event_id>/info/edit", methods=['GET','POST'])
def editEventInfo(event_id):
    editedEventInfo = session.query(Event).filter_by(id = event_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedEventInfo.name = request.form['name']
        if request.form['date']:
            editedEventInfo.date = request.form['date']
        if request.form['time']:
            editedEventInfo.time = request.form['time']
        if request.form['price']:
            editedEventInfo.price = request.form['price']
        if request.form['venue']:
            editedEventInfo.venue = request.form['venue']
        if request.form['description']:
            editedEventInfo.description = request.form['description']
        return redirect(url_for('showEventInfo', event_id = event_id))
    else:
        return render_template('editEventInfo.html', event = editedEventInfo)
    

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '127.0.0.1', port = 5050)
