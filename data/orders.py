import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "orders"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    owner_username = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.username")
    )
    event_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id")
    )
    event = orm.relationship("Event", back_populates="orders")
    # place = orm.relationship("Place", back_populates="orders")
    owner = orm.relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order> {self.id}: {self.event_id} (Event), {self.owner_username} (Owner)"
