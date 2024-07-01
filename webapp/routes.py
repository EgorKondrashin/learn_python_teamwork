from webapp import app
from flask import render_template, flash, redirect, url_for
from webapp.forms import LoginForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from webapp import db
from webapp.models import User


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', title='Brows')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли в личный кабинет')
            return redirect(url_for('index'))
    flash('Неверный email или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из личного кабинета')
    return redirect(url_for('index'))