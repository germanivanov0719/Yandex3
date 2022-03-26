import datetime as dt

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    created_datetime = Column(DateTime, default=dt.datetime.now)
    owner_username = Column(Integer, ForeignKey("users.username"))
    event_id = Column(Integer, ForeignKey("events.id"))
    event = orm.relationship("Event", back_populates="orders")
    owner = orm.relationship("User", back_populates="orders")

    def __repr__(self):
        return (
            f"<Order> {self.id}: {self.event_id} (Event),"
            f"{self.owner_username} (Owner)"
        )
