from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некоректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=100, message='Пароль должен быть не короче 5 символов')])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[Length(min=4, max=10, message="Им должно быть от 4 до 10 символов")])
    email = StringField('Email: ', validators=[Email('Некоректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=100, message='Пароль должен быть не короче 5 символов')])
    psw2 = PasswordField('Повтор пороля: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Регистарция')