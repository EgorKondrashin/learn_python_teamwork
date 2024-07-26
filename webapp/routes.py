from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from webapp import app, db
from webapp.forms import RegistrationForm, LoginForm, PriceForm
from webapp.models import User, Price, Schedule
from collections import defaultdict


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
            flash('Вы успешно вошли в личный кабинет!')
            return redirect(url_for('index'))
    flash('Неверный email или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из личного кабинета!')
    return redirect(url_for('index'))


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
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(url_for('register'))


@app.route('/about_me')
def about_me():
    return render_template('about_me.html', title='Немного о себе')


@app.route('/price_list')
def price_list():
    title = 'Стоимость услуг'
    price = Price.query.all()
    return render_template('price_list.html', title=title, price=price)


@app.route('/sign_up')
def sign_up_for_procedure():
    procedure = request.args.get('values')
    form = PriceForm()
    form.set_choices()
    form.procedure.default = [procedure]
    form.process()
    query_schedule = Schedule.query.where(Schedule.is_active==True).all()
    dict_schedule = defaultdict(list)
    for schedule in query_schedule:
        dict_schedule[schedule.split_schedule_date.strftime('%d.%m.%Y')].append(schedule.split_schedule_time.strftime('%H:%M'))

    for key, value in dict_schedule.items():
        print(key, value)

    return render_template('sign_up_procedure.html', form=form, list_date=list(dict_schedule.keys()))


@app.route('/process_sign_up', methods=["POST"])
def process_sign_up():
    form = PriceForm()
    form.set_choices()
    if form.validate_on_submit():
        flash(f'Вы выбрали: {form.procedure.data}')
        print(request.data)
        print(form.date.data)
    return redirect(url_for('index'))
