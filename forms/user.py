from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    username = StringField('Никнейм пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Создать')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
