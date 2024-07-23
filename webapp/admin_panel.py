import os
import flask_admin as admin
from flask import flash, url_for, redirect
from flask_admin import AdminIndexView, expose, helpers, form
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from webapp import app, db
from webapp.models import Price, Schedule
from webapp.forms import LoginAdminForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

file_path = os.path.abspath(os.path.dirname(__name__))


def name_gen_image(model, file_data):
    hash_name = f'{model.procedure}'
    return hash_name


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        if not current_user.is_admin:
            return redirect(url_for('index'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginAdminForm()
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user and user.check_password(form.password.data):
                login_user(user)
            else:
                flash('Неверный email или пароль')

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class PriceView(MyModelView):
    def scaffold_form(self):
        form_class = super(PriceView, self).scaffold_form()
        form_class.description = TextAreaField('Описание процедуры')
        return form_class

    form_args = {
        'procedure': dict(label='Название процедуры',
                          validators=[DataRequired()]),
        'description': dict(label='Описание процедуры',
                            validators=[DataRequired(), Length(max=500)]),
        'price': dict(label='Цена', validators=[DataRequired(), NumberRange()])
    }

    form_extra_fields = {
        'link_photo_by_procedure': form.ImageUploadField(
            '',
            base_path=os.path.join(file_path, 'webapp/static/price/'),
            url_relative_path='price/',
            namegen=name_gen_image,
            max_size=(700, 1280, True),
            thumbnail_size=(100, 100, True),
        )
    }

    def create_form(self, obj=None):
        return super(PriceView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(PriceView, self).edit_form(obj)


admin = admin.Admin(app, 'Brows', index_view=MyAdminIndexView(),
                    base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(PriceView(Price, db.session, name='Услуги'))
admin.add_view(MyModelView(Schedule, db.session, name='Расписание'))
