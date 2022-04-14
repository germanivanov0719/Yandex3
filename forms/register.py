from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    SubmitField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль", validators=[DataRequired()]
    )
    name = StringField("Полное имя", validators=[DataRequired()])
    about = TextAreaField("О себе")
    submit = SubmitField("Зарегистрироваться")
