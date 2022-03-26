import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True
    )
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_datetime = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    controlled_place_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("places.id")
    )

    controlled_place = orm.relationship(
        "Place", back_populates="controlling_users"
    )
    orders = orm.relationship("Order")

    def __repr__(self):
        return f"<User> {self.username}: {self.name}, {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
