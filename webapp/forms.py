from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from webapp import db
from webapp.models import User


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(),
                                                         Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(),
                                                         Email()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('''Пользователь с такой эл. почтой уже
                                  существует.''')
