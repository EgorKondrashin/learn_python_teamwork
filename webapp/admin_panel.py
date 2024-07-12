import flask_admin as admin
from flask import flash, url_for, redirect
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from webapp import app, db
from webapp.models import Price, Schedule
from webapp.forms import LoginAdminForm


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
        return current_user.is_authenticated


admin = admin.Admin(app, 'Brows', index_view=MyAdminIndexView(),
                    base_template='my_master.html', template_mode='bootstrap4')
admin.add_view(MyModelView(Price, db.session, name='Услуги'))
admin.add_view(MyModelView(Schedule, db.session, name='Расписание'))
