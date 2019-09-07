from flask import Flask, render_template
from sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/events'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
@app.route("/event")
def showEvent():
    return render_template('events.html')


@app.route("/event/new")
def newEvent():
    return render_template('newEvent.html')


@app.route("/event/<int:event_id>/edit")
def editEvent(event_id):
    return render_template('editEvent.html')


@app.route("/event/<int:event_id>/delete")
def deleteEvent(event_id):
    return render_template('deleteEvent.html')


@app.route("/event/<int:event_id>/")
@app.route("/event/<int:event_id>/attendance")
def showAttendance(event_id):
    return render_template('attendance.html')


@app.route("/event/<int:event_id>/attendance/new")
def newAttendance(event_id):
    return render_template('newAttendance.html  ')


@app.route("/event/<int:event_id>/attendance/<int:user_id>/edit")
def editAttendance(event_id):
    return "This page edit an existing attendance of an event"


@app.route("/event/<int:event_id>/attendance/<int:user_id>/delete")
def deleteAttendance(event_id):
    return "This page delete an existing attendance of an event"


if __name__ == "__main__":
    app.debug = True
    app.run(host = '127.0.0.1', port = 5050)
