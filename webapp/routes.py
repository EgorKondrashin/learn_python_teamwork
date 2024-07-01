from flask import flash, render_template, redirect, url_for
from flask_login import current_user
from webapp import app, db
from webapp.forms import RegistrationForm
from webapp.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Brows')


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/process-register', methods=['POST'])
def process_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            discount=15
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(url_for('register'))
