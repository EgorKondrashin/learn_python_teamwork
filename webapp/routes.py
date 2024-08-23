from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from webapp import app, db
from webapp.forms import RegistrationForm, LoginForm, PriceForm, ReviewForm
from webapp.models import User, Price, Schedule, Review, Appointment
from urllib.parse import urlsplit
from webapp.service import create_appointment_and_reservation_schedule


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
    next_page = request.args.get('next')
    return render_template('login.html', page_title=title, form=login_form, next=next_page)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    next_page = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if not next_page or urlsplit(next_page).netloc != '':
                flash('Вы успешно вошли в личный кабинет!')
                next_page = url_for('index')
            return redirect(next_page)
    flash('Неверный email или пароль')
    return redirect(url_for('login', next=next_page))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из личного кабинета!')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/about-me')
def about_me():
    return render_template('about_me.html', title='Немного о себе')


@app.route('/price-list')
def price_list():
    title = 'Стоимость услуг'
    price = Price.query.all()
    return render_template('price_list.html', title=title, price=price)


@app.route('/sign-up')
@login_required
def sign_up_for_procedure():
    title = 'Запись на процедуры'
    procedure = request.args.getlist('values')
    form = PriceForm()
    form.set_choices()
    form.procedure.default = procedure
    form.process()

    return render_template('sign_up_procedure.html', form=form, title=title)


@app.route('/process-sign-up', methods=["POST"])
@login_required
def process_sign_up():
    form = PriceForm()
    form.set_choices()
    # Использовать транзакцию
    if form.validate_on_submit():
        if not form.procedure.data:
            flash('Необходимо выбрать процедуру!')
            return redirect(url_for('sign_up_for_procedure', values=form.procedure.data))

        result = create_appointment_and_reservation_schedule(
            user_id=current_user.id,
            ids_procedure=form.procedure.data,
            id_date=form.date.data)

        if result is None:
            flash('Мастер не успеет вас принять, пожалуйста выберите другое время!')
            return redirect(url_for('sign_up_for_procedure', values=form.procedure.data))

        flash(f'Вы успешно записались! Дата записи: {result[0]}, \
              процедуры: {", ".join([p.procedure for p in result[1]])}')
    return redirect(url_for('index'))


@app.route('/new-review')
@login_required
def new_review():
    title = "Оставьте свой отзыв"
    review_form = ReviewForm()
    return render_template('new_review.html', page_title=title, form=review_form)


@app.route('/process-new-review', methods=['POST'])
def process_new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        tab_review = Review(
            body=form.body.data,
            user_id=current_user.id
        )
        db.session.add(tab_review)
        db.session.commit()
        return redirect(url_for('review'))


@app.route('/review')
def review():
    title = "Отзывы"
    page = request.args.get('page', 1, type=int)
    my_review = Review.query.order_by(Review.created_at.desc())
    reviews = db.paginate(my_review, page=page, per_page=app.config['REVIEW_PER_PAGE'], error_out=False)
    next_url = url_for('review', page=reviews.next_num) \
        if reviews.has_next else None
    prev_url = url_for('review', page=reviews.prev_num) \
        if reviews.has_prev else None
    return render_template('review.html', page_title=title, rev=reviews.items, next_url=next_url, prev_url=prev_url)


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', page_title='Портфолио')
