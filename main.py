import os

from flask import Flask
from flask_login import LoginManager

from data import db_session
from data.events import Event
from data.orders import Order
from data.places import Place
from data.users import User

app, login_manager, db = None, None, None


def main():
    global app, login_manager, db, load_user
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(12).hex()
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        return db.query(User).get(username)

    db_session.global_init("db/db.sqlite")
    db = db_session.create_session()
    import app_routes

    app.run(port=8000, host="127.0.0.1")


if __name__ == "__main__":
    main()
