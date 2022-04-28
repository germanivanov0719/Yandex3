from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class CreatePlaceForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    address = StringField("Адрес")
    about = TextAreaField("Описание")
    submit = SubmitField("Отправить на проверку")
