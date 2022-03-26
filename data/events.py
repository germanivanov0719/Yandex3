import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "events"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    place_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("places.id")
    )
    required_age = sqlalchemy.Column(sqlalchemy.Integer, default=14)
    notes = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    place = orm.relationship("Place", back_populates="events")
    orders = orm.relationship("Order", back_populates="event")

    def __repr__(self):
        return f"<Event> {self.id}: {self.name}, {self.place_id} (Place)"
