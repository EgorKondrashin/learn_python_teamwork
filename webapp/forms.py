from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectMultipleField, widgets, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, \
    Length
from wtforms_alchemy import PhoneNumberField
import sqlalchemy as sa
from webapp import db
from webapp.models import User, Price, Schedule


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
        render_kw={"class": "btn btn-primary btn-lg btn-block"})

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('''Пользователь с такой эл. почтой уже
                                  существует.''')


class ReviewForm(FlaskForm):
    body = TextAreaField('Ваш отзыв:', validators=[DataRequired(), Length(min=1, max=150)],
                             render_kw={"class": "form-control", "id": "exampleFormControlTextarea1", "rows": "4"})
    submit = SubmitField('Отправить',
                         render_kw={"class": "btn btn-primary btn-lg btn-block"})


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


class MyMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


class PriceForm(FlaskForm):
    procedure = MyMultipleField(label='')
    date = SelectField('Дата записи', validators=[DataRequired()])
    submit = SubmitField(
        'Записаться',
        render_kw={"class": "btn btn-lg btn-primary btn-block"}
    )

    def set_choices(self):
        self.procedure.choices = [(p.id, p.procedure) for p in Price.query.all()]
        self.date.choices = [(schedule.id, schedule.format_date) for schedule in Schedule.query.where(Schedule.is_active==True).order_by(Schedule.date_time_schedule).all()]
