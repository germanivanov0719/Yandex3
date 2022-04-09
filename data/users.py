import datetime as dt

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    about = Column(String, nullable=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=True)
    created_datetime = Column(DateTime, default=dt.datetime.now)
    controlled_place_id = Column(Integer, ForeignKey("places.id"))

    controlled_place = orm.relationship(
        "Place", back_populates="controlling_users"
    )
    orders = orm.relationship("Order")

    def __repr__(self):
        return f"<User> {self.email}: {self.name}, {self.id}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(
            str(password) + str(self.email)
        )

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password, str(password) + str(self.email)
        )
