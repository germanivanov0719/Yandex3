# Remove when in production
import datetime
import os

from data import db_session
from data.places import Place
from data.users import User
from data.orders import Order
from data.events import Event


def clear_db():
    try:
        os.remove("db/db.sqlite")
    except Exception:
        print("Error testing database")


def test_db():
    db_sess = db_session.create_session()

    # User
    user = User(
        username="testuser",
        name="User1",
        about="I'm a user1",
        email="testuser@users.com",
    )
    user.set_password("123")
    db_sess.add(user)
    # Place
    place = Place(
        name="Place1", address="On Earth", about="It is a great place"
    )
    db_sess.add(place)
    # Place controlled
    user = db_sess.query(User).first()
    user.controlled_place_id = db_sess.query(Place).first().id
    # Event
    event = Event(
        name="the Great Event",
        description="the greatest event ever held",
        datetime=datetime.datetime.now(),
        place=place,
    )
    # Order
    order = Order(event=event, owner=user)
    db_sess.add(order)
    # Commit
    db_sess.commit()
