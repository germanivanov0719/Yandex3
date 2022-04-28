from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    TextAreaField,
    IntegerField,
    DateTimeField,
)
from wtforms.validators import DataRequired


class CreateEventForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    datetime = DateTimeField("Дата и время проведения")
    required_age = IntegerField("Минимальный возраст")
    description = TextAreaField("Описание")
    notes = TextAreaField("Примечания")
    submit = SubmitField("Создать")
