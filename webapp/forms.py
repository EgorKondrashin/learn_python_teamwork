from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms_alchemy import PhoneNumberField
import sqlalchemy as sa
from webapp import db
from webapp.models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Электронная почта',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня',
                               render_kw={"class": "form-check-input"})
    submit = SubmitField(
        'Войти',
        render_kw={"class": "btn btn-lg btn-primary btn-block"})


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    email = StringField('Электронная почта',
                        validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"}
                        )
    phone = PhoneNumberField('Номер телефона', validators=[DataRequired()],
                             region='RU', render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={"class": "btn btn-lg btn-primary btn-block"})

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('''Пользователь с такой эл. почтой уже
                                  существует.''')


class ReviewForm(FlaskForm):
    body = TextAreaField('Ваш отзыв:', validators=[DataRequired(), Length(min=1, max=150)],
                             render_kw={"class": "form-control", "id":"exampleFormControlTextarea1", "rows":"3"})
    submit = SubmitField('Отправить',
                         render_kw={"class": "btn btn-lg btn-primary btn-block"})

    
class LoginAdminForm(FlaskForm):
    email = StringField(
        'Электронная почта',
        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Неправильное имя пользователя')

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()
