from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, \
    Regexp
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
    pattern = r'\+7\s?[\(]{0,1}9[0-9]{2}[\)]{0,1}\s?\d{3}[-]{0,1}\d{2}[-]{0,1}\d{2}'
    first_name = StringField('Имя', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    email = StringField('Электронная почта',
                        validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"}
                        )
    phone = StringField(
        'Номер телефона',
        validators=[DataRequired(), Regexp(pattern, message='Введен некорректный номер телефона')],
        render_kw={"class": "form-control"}
    )
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Зарегистрироваться',
                         render_kw={"class": "btn btn-lg btn-primary btn-block"})

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('''Пользователь с такой эл. почтой уже
                                  существует.''')
