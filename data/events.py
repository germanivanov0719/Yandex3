import datetime as dt

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_datetime = Column(DateTime, default=dt.datetime.now)
    datetime = Column(DateTime)
    place_id = Column(Integer, ForeignKey("places.id"))
    required_age = Column(Integer, default=14)
    notes = Column(String, nullable=True)

    place = orm.relationship("Place", back_populates="events")
    orders = orm.relationship("Order", back_populates="event")

    def __repr__(self):
        return f"<Event> {self.id}: {self.name}, {self.place_id} (Place)"
