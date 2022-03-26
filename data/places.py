import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Place(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "places"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )

    controlling_users = orm.relationship(
        "User", back_populates="controlled_place"
    )
    # orders = orm.relationship("Order")
    events = orm.relationship("Event")

    def __repr__(self):
        return f"<Place> {self.id}: {self.name}, {self.address}"

    # def set_password(self, password):
    #     self.hashed_password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.hashed_password, password)
