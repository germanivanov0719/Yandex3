import os

from flask import Flask, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import db_tests
from data import db_session
from data.events import Event
from data.orders import Order
from data.places import Place
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12).hex()

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_tests.clear_db()
    db_session.global_init("db/db.sqlite")
    db_tests.test_db()
    app.run(port=8000, host="127.0.0.1")


@login_manager.user_loader
def load_user(username):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(username)


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    main()
