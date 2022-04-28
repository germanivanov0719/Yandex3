from __main__ import app, db
from copy import copy  # pylint: disable=E0611
from flask import redirect, render_template, abort
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException

from data.events import Event
from data.orders import Order
from data.places import Place
from data.users import User
from forms.edit_profile import EditProfileForm
from forms.create_event import CreateEventForm
from forms.create_place import CreatePlaceForm
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
    places = db.query(Place).filter(Place.visibility).all()
    return render_template("places.html", places=places, active="places")


@app.route("/event/<int:id>")
def event_info(id):
    event = db.query(Event).filter(Event.id == id).first()
    if event is None:
        abort(404)
    try:
        datetime = event.datetime.strftime("%H:%M %d.%m.%y")
    except:
        datetime = "время не указано"
    return render_template("event_info.html", event=event, datetime=datetime)


@app.route("/place/<int:id>")
def place_info(id):
    place = db.query(Place).filter(Place.id == id).first()
    if place is None:
        abort(404)
    orders = list(db.query(Order).filter().all())
    ord2 = []
    for o in orders:
        if not ((o.event.place != place) or o.is_fulfilled or o.is_declined):
            ord2.append(o)
    return render_template("place_info.html", place=place, orders=ord2)


@app.route("/profile")
def profile_info():
    if not current_user:
        return redirect("/")
    return render_template("profile.html", user=current_user)


@app.route("/edit", methods=["POST", "GET"])
def edit_profile():
    form = EditProfileForm()
    if not current_user.is_authenticated:
        return redirect("/")
    id = current_user.id
    user = db.query(User).filter(User.id == id).first()
    old_user = copy(user)
    if form.validate_on_submit():
        if (
            form.password.data != ""
            and form.password.data == form.password_again.data
        ):
            user.set_password(form.password.data)
        elif (
            form.password.data != ""
            and form.password.data != form.password_again.data
        ):
            return render_template(
                "edit_profile.html",
                title="Изменение профиля",
                form=form,
                message="Пароли не совпадают",
            )
            # if not(db.query(User).filter(current_user.email == form.email.data).first()):
        if (
            form.email.data != ""
            and user.email != form.email.data
            and not (
                db.query(User).filter(User.email == form.email.data).first()
            )
        ):
            return render_template(
                "register.html",
                title="Изменение профиля",
                form=form,
                message="Такая почта уже используется",
            )
        user.name = form.name.data if form.name.data != "" else user.name
        user.email = form.email.data if form.email.data != "" else user.email
        user.about = form.about.data if form.about.data != "" else user.about
        db.delete(old_user)
        db.add(user)
        db.flush()
        db.commit()
        return redirect("/profile")
    return render_template(
        "edit_profile.html", title="Изменение профиля", form=form
    )


@app.route("/buy/event/<int:id>")
def buy_event(id):
    if not current_user.is_authenticated:
        return redirect("/login")
    event = db.query(Event).filter(Event.id == id).first()
    if event is None:
        abort(404)
    return render_template("buy.html", event=event)


@app.route("/finish-order/event/<int:id>/<int:q>")
def finish_order_event(id, q):
    if db.query(Event).filter(Event.id == id).first() is None:
        abort(504)
    if current_user.is_authenticated:
        for _ in range(q):
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


@app.route("/create-place", methods=["GET", "POST"])
def create_place():
    if not current_user.is_authenticated:
        return redirect("/login")
    form = CreatePlaceForm()
    if form.validate_on_submit():
        if current_user.controlled_place:
            return render_template(
                "create_place.html",
                title="Создание места",
                form=form,
                message="Ваш аккаунт уже привязан к месту. Попробуйте создать новый.",
            )
        if db.query(Place).filter(Place.name == form.name.data).first():
            return render_template(
                "create_place.html",
                title="Создание места",
                form=form,
                message="Место с таким названием уже есть",
            )
        p = Place(
            name=form.name.data,
            address=form.address.data,
            about=form.about.data,
        )
        db.add(p)
        current_user.controlled_place = p
        db.flush()
        db.commit()
        return redirect("/")
    return render_template(
        "create_place.html", title="Создание места", form=form
    )


@app.route("/create-event", methods=["GET", "POST"])
def create_event():
    if not current_user.is_authenticated:
        return redirect("/login")
    form = CreateEventForm()
    if form.validate_on_submit():
        if not current_user.controlled_place:
            return render_template(
                "create_event.html",
                title="Создание мероприятия",
                form=form,
                message="Ваш аккаунт не привязан к месту. Попробуйте создать его.",
            )
        if db.query(Event).filter(Event.name == form.name.data).first():
            return render_template(
                "create_event.html",
                form=form,
                message="Событие с таким названием уже есть",
            )
        e = Event(
            name=form.name.data,
            required_age=form.required_age.data,
            datetime=form.datetime.data,
            description=form.description.data,
            notes=form.notes.data,
        )
        e.place = current_user.controlled_place
        db.add(e)
        db.flush()
        db.commit()
        return redirect("/")
    return render_template(
        "create_event.html", title="Создание мероприятия", form=form
    )


@app.route("/accept/<int:id>")
def accept(id):
    o = db.query(Order).filter(Order.id == id).first()
    if o is None:
        abort(404)
    o.is_fulfilled = True
    o.is_declined = False
    db.flush()
    db.commit()
    return redirect("/place/" + str(o.event.place.id))


@app.route("/decline/<int:id>")
def decline(id):
    o = db.query(Order).filter(Order.id == id).first()
    if o is None:
        abort(404)
    o.is_fulfilled = False
    o.is_declined = True
    db.flush()
    db.commit()
    return redirect("/place/" + str(o.event.place.id))


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
