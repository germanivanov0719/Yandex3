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
    name = StringField("Имя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    about = TextAreaField("О себе")
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль", validators=[DataRequired()]
    )
    submit = SubmitField("Подтвердить изменения")

