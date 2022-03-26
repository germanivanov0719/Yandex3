from flask import Flask, render_template

from data import db_session
from data.places import Place
from data.users import User
from data.orders import Order
from data.events import Event

import db_tests


from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "tickets_app_key"

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
