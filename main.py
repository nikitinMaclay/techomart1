import datetime

from flask import Flask, render_template, redirect, request, make_response, abort, jsonify

from data import db_session

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
#     days=365
# )
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    # if form.validate_on_submit():
    #     if form.password.data != form.password_again.data:
    #         return render_template('register.html', title='Регистрация',
    #                                form=form,
    #                                message="Пароли не совпадают")
    return render_template('register.html', title='Регистрация', form=form)


def main():

    app.run()


if __name__ == '__main__':
    main()
