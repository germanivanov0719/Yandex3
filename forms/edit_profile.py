from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    SubmitField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField("Имя")
    email = EmailField("Почта")
    about = TextAreaField("О себе")
    password = PasswordField("Пароль")
    password_again = PasswordField("Повторите пароль")
    submit = SubmitField("Подтвердить изменения")
