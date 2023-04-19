import datetime

from flask import Flask, render_template, redirect, request, make_response, abort, jsonify

from data import db_session
from data.users import User

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog():
    return render_template("catalog.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   heading="Создание профиля")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   heading="Создание профиля")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form,
                           heading="Создание профиля")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/user_profile', methods=["GET", "POST"])
@login_required
def user_profile():
    form = RegisterForm()
    if request.method == "GET":
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.password.data = current_user.password
    else:
            abort(404)
    return render_template('user_profile.html', title='Мой профиль', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_job():
    form = RegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.username.data = user.username
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Редактирование профиля',
                                   form=form,
                                   message="Пароли не совпадают",
                                   heading="Редактирование профиля")
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html',
                           title='Редактирование профиля',
                           form=form,
                           heading="Редактирование профиля"
                           )


def main():
    db_session.global_init("databases/technomart.db")
    app.run()


if __name__ == '__main__':
    main()
