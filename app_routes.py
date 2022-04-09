from flask import Flask, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from main import app


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")
