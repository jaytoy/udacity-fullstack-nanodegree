from flask_login import UserMixin

from app import db


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    date = db.Column(db.Date, nullable=True)
    time = db.Column(db.Time, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    venue = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=False)

    def __init__(self, name, date, time, price, venue, description):
        self.name = name
        self.date = date
        self.time = time
        self.price = price
        self.venue = venue
        self.description = description

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'date': self.date,
            'time': self.time.isoformat(),
            'price': self.price,
            'venue': self.venue,
            'description': self.description
        }



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)

    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        user = db.session.query(User).filter_by(id = user_id).one_or_none()
        return user
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }
