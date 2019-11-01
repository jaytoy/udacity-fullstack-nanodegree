from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Event

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
    return render_template('events.html')


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
def showAttendance(event_id):
    render_template('eventInfo.html')


#Create a new attendance for the event
@app.route("/event/<int:event_id>/info/new", methods=['GET','POST'])
def newAttendance(event_id):
    render_template('newEventInfo.html')


@app.route("/event/<int:event_id>/info/<int:info_id>/edit", methods=['GET','POST'])
def editAttendance(event_id, info_id):
    render_template('editEventInfo.html')
    
 
@app.route("/event/<int:event_id>/info/<int:info_id>/delete", methods = ['GET','POST'])
def deleteAttendance(event_id, attendance_id):
    render_template('deleteEventInfo.html')
    


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '127.0.0.1', port = 5050)
