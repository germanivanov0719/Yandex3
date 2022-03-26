import datetime as dt

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Place(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    about = Column(String, nullable=True)
    created_datetime = Column(DateTime, default=dt.datetime.now)

    controlling_users = orm.relationship(
        "User", back_populates="controlled_place"
    )
    events = orm.relationship("Event")

    def __repr__(self):
        return f"<Place> {self.id}: {self.name}, {self.address}"
