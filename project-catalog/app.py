import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

from models import *


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content. "
    + '<a href="/login">Login</a>', 403


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, events=[]
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("showEvent"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("showEvent"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Show all events
@app.route("/")
@app.route("/event", methods=['GET', 'POST'])
def showEvent():
    if request.method == 'GET':
        events = db.session.query(Event).order_by(Event.date)
        return render_template('events.html', events=events)


# Create a new event
@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def newEvent():
    if request.method == 'POST':
        newEvent = Event(
            name=request.form['name'],
            date=request.form['date'],
            time=request.form['time'],
            price=request.form['price'],
            venue=request.form['venue'],
            description=request.form['description'],
            user_id=current_user.id
        )
        db.session.add(newEvent)
        db.session.commit()
        return redirect(url_for('showEvent'))
    else:
        return render_template('newEvent.html')


# Edit an event
@app.route("/event/<int:event_id>/edit", methods=['GET', 'POST'])
@login_required
def editEvent(event_id):
    editedEvent = session.query(Event).filter_by(id=event_id).one()
    if current_user.id != editedEven.user_id:
        return "You are not authorized to edit this event."
    else:
        editedEvent = session.query(Event).filter_by(id=event_id).one()
        if request.method == 'POST':
            if request.form['name']:
                editedEvent.name = request.form['name']
                return redirect(url_for('showEvent'))
        else:
            return render_template('editEvent.html', event=editedEvent)


# Delete an event
@app.route("/event/<int:event_id>/delete", methods=['GET', 'POST'])
@login_required
def deleteEvent(event_id):
    eventToDelete = db.session.query(Event).filter_by(id=event_id).one()
    if current_user.id != eventToDelete.user_id:
        return "You are not authorized to delete this event."
    else:
        if request.method == 'POST':
            db.session.delete(eventToDelete)
            db.session.commit()
            return redirect(url_for('showEvent', event_id=event_id))
        else:
            return render_template('deleteEvent.html', event=eventToDelete)

# Show the information of an event
@app.route("/event/<int:event_id>/")
@app.route("/event/<int:event_id>/info")
def showEventInfo(event_id):
    event = db.session.query(Event).filter_by(id=event_id).one()
    return render_template('eventInfo.html', event=event)

# Edit the information of an event
@app.route("/event/<int:event_id>/info/edit", methods=['GET', 'POST'])
@login_required
def editEventInfo(event_id):
    editedEventInfo = db.session.query(Event).filter_by(id=event_id).one()
    if current_user.id != editedEventInfo.user_id:
        return "You are not authorized to edit this event."
    else:
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
            return redirect(url_for('showEventInfo', event_id=event_id))
        else:
            return render_template('editEventInfo.html', event=editedEventInfo)


@app.route('/event/JSON')
def eventsJSON():
    """Return JSON for all the events"""
    events = db.session.query(Event).all()
    return jsonify(events=[e.serialize for e in events])


@app.route('/event/<int:event_id>/JSON')
def eventJSON(event_id):
    """Return JSON for an event"""
    event = db.session.query(Event).filter_by(id=event_id).one()
    return jsonify(event=event.serialize)


@app.route('/user/JSON')
def usersJSON():
    """Return JSON for all the users"""
    users = db.session.query(User).all()
    return jsonify(users=[u.serialize for u in users])


@app.route('/user/<string:user_id>/JSON')
def userJSON(user_id):
    """Return JSON for an user """
    user = db.session.query(User).filter_by(id=user_id).one()
    return jsonify(user=user.serialize)


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5050, ssl_context="adhoc")
