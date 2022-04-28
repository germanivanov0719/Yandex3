from __main__ import app, db  # pylint: disable=E0611
from flask import redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException

from data.events import Event
from data.orders import Order
from data.places import Place
from data.users import User
from forms.edit_profile import EditProfileForm
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


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_profile(id):
    form = EditProfileForm()
    if not current_user:
        return redirect("/")
    user = db.query(User).filter(User.id == id).first()
    old_user = user
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "edit_profile.html",
                title="Изменение профиля",
                form=form,
                message="Пароли не совпадают",
            )
            # if not(db.query(User).filter(current_user.email == form.email.data).first()):
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Изменение профиля",
                form=form,
                message="Такой пользователь уже есть",
            )
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.hashed_password = form.password.data
        db.delete(old_user)
        db.add(user)
        db.commit()
        return redirect("/profile")
    return render_template(
        "edit_profile.html", title="Изменение профиля", form=form
    )
    # if not current_user:
    #     return redirect("/")
    # user = current_user
    # user.name = request.form.get("name")
    # user.about = request.form.get("about")
    # user.hashed_password = request.form.get("new_pass")
    # user.email = request.form.get("email")
    # if user.email in db.query(User.email).all():
    #     # error warning
    #     pass
    # db.commit()
    # return render_template("profile_edit.html", user=user)


@app.route("/buy/event/<int:id>")
def buy_event(id):
    if not current_user.is_authenticated:
        return redirect("/login")
    event = db.query(Event).filter(Event.id == id).first()
    return render_template("buy.html", event=event)


@app.route("/finish-order/event/<int:id>/<int:q>")
def finish_order_event(id, q):
    if current_user.is_authenticated:
        for i in range(q):
            order = Order(owner=current_user, event_id=id)
            db.add(order)
        db.commit()
    return redirect("/")


@app.route("/tickets")
def tickets():
    if current_user.is_authenticated:
        ord = db.query(Order).filter(Order.owner == current_user).all()
        unused = sorted(
            [t for t in ord if not t.is_used],
            key=lambda t: t.created_datetime,
            reverse=True,
        )
        used = sorted(
            [t for t in ord if t.is_used],
            key=lambda t: t.created_datetime,
            reverse=True,
        )
        print(*unused, "\n", *used)
        return render_template(
            "tickets.html", active="tickets", used=used, unused=unused
        )
    return redirect("/login")


@app.route("/tickets/mark/<int:id>")
def mark(id):
    if current_user.is_authenticated:
        t = (
            db.query(Order)
            .filter(Order.owner == current_user)
            .filter(Order.id == id)
            .first()
        )
        t.is_used = not t.is_used
        db.commit()
        return redirect("/tickets")
    return redirect("/login")


@app.errorhandler(404)
def error404(e):
    return render_template("error404.html"), 404


@app.errorhandler(Exception)
def handle_unknown_error(e):
    if isinstance(e, HTTPException):
        return (
            render_template("other_error.html", e=e.code, error=str(e)),
            e.code,
        )
    else:
        return (
            render_template("other_error.html", e=str(type(e)), error=str(e)),
            500,
        )
