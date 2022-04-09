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
    except FileNotFoundError:
        pass
    except Exception:
        raise AssertionError("Unable to remove database")


def test_db():
    clear_db()
    db_session.global_init("db/db.sqlite")
    db_sess = db_session.create_session()
    assert db_sess != 0
    # User
    user = User(
        name="User1",
        about="I'm a user1",
        email="testuser@users.com",
    )
    user.set_password("123")
    assert user != 0
    db_sess.add(user)
    # Place
    place = Place(
        name="Place1", address="On Earth", about="It is a great place"
    )
    assert place != 0
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
    assert event != 0
    # Order
    order = Order(event=event, owner=user)
    assert order
    db_sess.add(order)
    # Commit
    db_sess.commit()
    assert db_sess != 0


if __name__ == "__main__":
    test_db()
