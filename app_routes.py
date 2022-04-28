from __main__ import app, db  # pylint: disable=E0611
from flask import redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException

from data.events import Event
from data.orders import Order
from data.places import Place
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    events = db.query(Event).all()
    return render_template("index.html", events=events, active="index")


@app.route("/events")
@app.route("/events.html")
def events():
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.query(User).filter(User.email == form.email.data).first()
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
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        if db.query(User).filter(User.email == form.email.data).first():
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
        db.add(user)
        db.commit()
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
    places = db.query(Place).all()
    return render_template("places.html", places=places, active="places")


@app.route("/event/<int:id>")
def event_info(id):
    event = db.query(Event).filter(Event.id == id).first()
    try:
        datetime = event.datetime.strftime("%H:%M %d.%m.%y")
    except:
        datetime = "время не указано"
    return render_template("event_info.html", event=event, datetime=datetime)


@app.route("/place/<int:id>")
def place_info(id):
    place = db.query(Place).filter(Place.id == id).first()
    db.commit()
    return render_template("place_info.html", place=place)


@app.route("/profile")
def profile_info():
    if not current_user:
        return redirect("/")
    return render_template("profile.html", user=current_user)


@app.route("/profile/edit", methods=["POST", "GET"])
def edit_profile():
    if not current_user:
        return redirect("/")
    user = current_user
    user.name = request.form.get("name")
    user.about = request.form.get("about")
    user.hashed_password = request.form.get("new_pass")
    user.email = request.form.get("email")
    if user.email in db.query(User.email).all():
        # error warning
        pass
    db.commit()
    # return render_template("profile_edit.html", user=user)


@app.route("/buy/event/<int:id>")
def buy_event(id):
    if not current_user.is_authenticated:
        return redirect("/login")
    event = db.query(Event).filter(Event.id == id).first()
    return render_template("buy.html", event=event)


@app.route("/finish-order/event/<int:id>")
def finish_order_event(id):
    if current_user.is_authenticated:
        order = Order(owner=current_user, event_id=id)
        db.add(order)
        db.commit()
    return redirect("/")


@app.errorhandler(404)
def error404(e):
    return render_template("error404.html"), 404


@app.errorhandler(Exception)
def handle_unknown_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template("other_error.html", code=code, error=str(e)), e.code
