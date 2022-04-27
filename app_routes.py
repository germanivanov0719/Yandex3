from __main__ import app  # pylint: disable=E0611
from flask import redirect, render_template, make_response, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from data import db_session
from data.users import User
from data.places import Place
from data.events import Event
from forms.login import LoginForm
from forms.register import RegisterForm


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    db_sess = db_session.create_session()
    events = db_sess.query(Event).all()
    return render_template("index.html", events=events, active="index")


@app.route("/events")
@app.route("/events.html")
def events():
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User(
            name=form.name.data, email=form.email.data, about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/places")
@app.route("/places.html")
def places():
    db_sess = db_session.create_session()
    places = db_sess.query(Place).all()
    return render_template("places.html", places=places, active="places")


@app.route("/event/<int:id>")
def event_info(id):
    db_sess = db_session.create_session()
    event = db_sess.query(Event).filter(Event.id == id).first()
    try:
        datetime = event.datetime.strftime("%H:%M %d.%m.%y")
    except:
        datetime = "время не указано"
    return render_template("event_info.html", event=event, datetime=datetime)


@app.route("/place/<int:id>")
def place_info(id):
    db_sess = db_session.create_session()
    place = db_sess.query(Place).filter(Place.id == id).first()
    return render_template("place_info.html", place=place)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)
