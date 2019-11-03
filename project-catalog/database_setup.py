import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)
    price = Column(Integer, nullable=True)
    venue = Column(String(250), nullable=True)
    description = Column(String(250), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    

engine = create_engine(
    "postgresql://postgres:1234@localhost/events",
    isolation_level="READ UNCOMMITTED"
)


Base.metadata.create_all(engine)
