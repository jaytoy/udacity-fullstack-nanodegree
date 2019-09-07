import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Attendance(Base):
    __tablename__ = 'attendance'

    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    pax = Column(String(8))
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship(Event)


engine = create_engine(
    "postgresql://postgres:1234@localhost/events",
    isolation_level="READ UNCOMMITTED"
)


Base.metadata.create_all(engine)