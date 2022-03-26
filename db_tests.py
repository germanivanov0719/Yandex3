from data import db_session
from data.places import Place
from data.users import User
from data.orders import Order
from data.events import Event


def clear_db():
    # Remove when in production
    import os

    try:
        os.remove("db/db.sqlite")
    except Exception:
        pass


def test_db():
    # Remove when in production
    import datetime

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
    # user = db_sess.query(User).first()
    # place = (
    #     db_sess.query(Place)
    #     .filter(Place.id == user.controlled_place_id)
    #     .first()
    # )
    order = Order(event=event, owner=user)
    # Commit
    db_sess.commit()
