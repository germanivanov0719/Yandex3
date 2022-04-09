import os

from flask import Flask, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import tests.db_tests as db_tests
from data import db_session
from data.users import User
from data.orders import Order
from data.places import Place
from data.events import Event


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12).hex()

login_manager = LoginManager()
login_manager.init_app(app)


import app_routes


def main():
    db_tests.clear_db()
    db_session.global_init("db/db.sqlite")
    db_tests.test_db()
    app.run(port=8000, host="127.0.0.1")


@login_manager.user_loader
def load_user(username):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(username)


if __name__ == "__main__":
    main()
