import datetime
import os

from data import db_session

from data.places import Place
from data.users import User
from data.orders import Order
from data.events import Event


def test_preparation():
    try:
        os.remove("db/db.sqlite")
    except FileNotFoundError:
        pass
    except Exception:
        raise AssertionError("Unable to remove database")


def test_init_db():
    db_session.global_init("db/db.sqlite")
    db_sess = db_session.create_session()
    assert db_sess != 0
    db_sess.commit()


def test_user():
    db_sess = db_session.create_session()
    user = User(
        name="User1",
        about="userabout",
        email="testuser@users.com",
    )
    db_sess.add(user)
    user = (
        db_sess.query(User).filter(User.email == "testuser@users.com").first()
    )
    user.set_password("123")
    assert user
    assert user.about == "userabout"
    assert user.email == "testuser@users.com"
    assert isinstance(user.id, int)
    assert user.check_password("123")
    db_sess.commit()


def test_place():
    db_sess = db_session.create_session()
    place = Place(
        name="Place1", address="OnEarth", about="It is a great place"
    )
    db_sess.add(place)
    place = db_sess.query(Place).filter(Place.name == "Place1").first()
    assert place
    assert place.name == "Place1"
    assert place.address == "OnEarth"
    assert place.about == "It is a great place"
    db_sess.commit()


def test_place_controlled_by():
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    user.controlled_place_id = db_sess.query(Place).first().id
    db_sess.commit()
    assert user.controlled_place


def test_event():
    db_sess = db_session.create_session()
    place = db_sess.query(Place).filter(Place.name == "Place1").first()
    event = Event(
        name="Event1",
        description="the greatest event ever held",
        datetime=datetime.datetime.now(),
        place=place,
    )
    event = db_sess.query(Event).filter(Event.name == "Event1").first()
    assert event
    assert event.description == "the greatest event ever held"
    assert event.datetime
    assert event.place == place
    assert event.required_age == 14
    db_sess.commit()

    db_sess.commit()


def test_order():
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.name == "Event1").first()
    user = (
        db_sess.query(User).filter(User.email == "testuser@users.com").first()
    )
    order = Order(event=event, owner=user)
    assert order
    db_sess.add(order)
    order = db_sess.query(Order).first()
    assert order
    db_sess.commit()


def test_cleanup():
    try:
        os.remove("db/db.sqlite")
    except Exception:
        raise AssertionError("Unable to remove database")
