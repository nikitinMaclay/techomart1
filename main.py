import datetime

from flask import Flask, render_template, redirect, request, make_response, abort, jsonify
from sqlalchemy import collate, func
from sqlalchemy.sql import text

from data import db_session, products_resources, producers_recources
from data.users import User
from data.products import Products
from data.users_products import UsersProducts
from data.users_cart_products import UsersCartProducts
from data.functions import word_separation

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from flask_restful import Api

from forms.user import RegisterForm, LoginForm
from forms.filtering import FilteringForm
from forms.product import ProductForm

import pymorphy2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.route("/", methods=["GET", "POST"])
@app.route("/")
@app.route("/index")
def index():
    form = ProductForm()
    if form.validate_on_submit():
        page_idx = 1
        db_sess = db_session.create_session()
        product = form.product.data
        product = word_separation(product)
        print(product)
        goods = db_sess.query(Products).filter(
            Products.id > 9 * (page_idx - 1), Products.id <= 9 * page_idx,
            func.lower(Products.name).like(func.lower(f"%{product}%"))).all()
        print(goods)
        for el in goods:
            print(el)
        goods_count = db_sess.query(Products).filter(
            Products.name.like(f'%{product}%')).count()
        if float(goods_count // 9) == goods_count / 9:
            goods_count = goods_count // 9
        else:
            goods_count = goods_count // 9 + 1
        print(goods_count)
        return render_template("catalog.html", goods=goods,
                               current_page=page_idx, goods_count=goods_count)
    return render_template("index.html", form=form)
    db_sess = db_session.create_session()
    goods = db_sess.query(Products).filter(Products.id >= 1, Products.id <= 4).all()
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        bookmarks_goods = db_sess.query(UsersProducts).filter(UsersProducts.user_id == current_user.id).all()
        bookmarks_count = len(bookmarks_goods)
        cart_goods = db_sess.query(UsersCartProducts).filter(UsersCartProducts.user_id == current_user.id).all()
        cart_count = len(cart_goods)
    else:
        bookmarks_count = 0
        cart_count = 0
    return render_template("index.html", goods=goods, bookmarks_count=bookmarks_count, cart_count=cart_count)


@app.route("/add_to_bookmarks", methods=['post'])
def add_to_bookmarks():
    if current_user.is_authenticated:
        page_idx = request.args.get("current_pg")
        good_id = request.args.get("good_id")
        db_sess = db_session.create_session()
        users_products = UsersProducts()
        users_products.user_id = current_user.id
        users_products.product_id = good_id
        try:
            db_sess.add(users_products)
            db_sess.commit()
        except:
            pass
        return redirect(f"/catalog/{page_idx}")
    else:
        return redirect(f"/login")


@app.route("/delete_from_bookmarks", methods=['post'])
def delete_from_bookmarks():
    good_id = request.args.get("good_id")
    db_sess = db_session.create_session()
    users_products = db_sess.query(UsersProducts).filter(UsersProducts.user_id == current_user.id,
                                                         UsersProducts.product_id == good_id).first()
    db_sess.delete(users_products)
    db_sess.commit()

    return redirect("/bookmark")


@app.route("/delete_from_cart", methods=['post'])
def delete_from_cart():
    good_id = request.args.get("good_id")
    db_sess = db_session.create_session()
    users_cart_products = db_sess.query(UsersCartProducts).filter(UsersCartProducts.user_id == current_user.id,
                                                                  UsersCartProducts.cart_product_id == good_id).first()
    db_sess.delete(users_cart_products)
    db_sess.commit()

    return redirect("/cart")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
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
    return render_template('register.html', title='Регистрация', form=form)


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
def edit_user():
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


@app.route('/catalog/<int:page_idx>', methods=["GET", "POST"])
def catalog(page_idx=1):
    filtering_form = FilteringForm()
    if filtering_form.validate_on_submit():
        producers = list(
            map(lambda i: i.label.text.lower(), filter(
                lambda i: i.data,
                [
                    filtering_form.bosch_producer,
                    filtering_form.dewalt_producer,
                    filtering_form.HITACHI_producer,
                    filtering_form.interscol_producer,
                    filtering_form.makita_producer
                ]
            ))
        )
        params = {
            'price_from': filtering_form.price_from.data,
            'price_to': filtering_form.price_to.data,
            'producers': ",".join(producers) if producers else "all"
        }
        return redirect(f"/catalog/1?{'&'.join(f'{i}={params[i]}' for i in params)}")

    db_sess = db_session.create_session()
    price_from = request.args.get('price_from', 0, int)
    price_to = request.args.get('price_to', max(db_sess.query(Products).all(), key=lambda i: i.price).price, int)
    producers = request.args.get('producers', 'all', str)

    goods = list(filter(
        lambda i: i.producer.name.lower() in producers if producers != 'all' else True,
        db_sess.query(Products).filter(price_from <= Products.price, Products.price <= price_to).all()
    ))
    goods_count = len(goods)
    if float(goods_count // 9) == goods_count / 9:
        goods_count = goods_count // 9
    else:
        goods_count = goods_count // 9 + 1

    if current_user.is_authenticated:
        bookmarks_goods = db_sess.query(UsersProducts).filter(UsersProducts.user_id == current_user.id).all()
        bookmarks_count = len(bookmarks_goods)
        cart_goods = db_sess.query(UsersCartProducts).filter(UsersCartProducts.user_id == current_user.id).all()
        cart_count = len(cart_goods)
    else:
        bookmarks_count = 0
        cart_count = 0
    goods = goods[9 * (page_idx - 1):page_idx * 9]

    return render_template(
        "catalog.html",
        goods=goods,
        current_page=page_idx,
        goods_count=goods_count,
        form=filtering_form,
        min_price=price_from,
        max_price=price_to,
        max_value=max(db_sess.query(Products).all(), key=lambda i: i.price).price,
        producers=producers,
        bookmarks_count=bookmarks_count,
        cart_count=cart_count
    )


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route("/bookmark")
def bookmark():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        goods = user.products

        goods_count = len(goods)

        cart_goods_count = len(user.cart_products)

        return render_template("bookmark.html", goods=goods, goods_count=goods_count, cart_goods_count=cart_goods_count)

    else:
        return redirect("/login")


@app.route("/cart")
def cart():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        goods = user.cart_products

        cart_goods_count = len(goods)

        goods_count = len(user.products)

        return render_template("cart.html", goods=goods, cart_goods_count=cart_goods_count, goods_count=goods_count)

    else:
        return redirect("/login")


@app.route("/add_to_cart", methods=['post'])
def add_to_cart():
    if current_user.is_authenticated:
        page_idx = request.args.get("current_pg")
        good_id = request.args.get("good_id")
        db_sess = db_session.create_session()
        users_cart_products = UsersCartProducts()
        users_cart_products.user_id = current_user.id
        users_cart_products.cart_product_id = good_id
        try:
            db_sess.add(users_cart_products)
            db_sess.commit()
        except:
            pass
        return redirect(f"/catalog/{page_idx}")
    else:
        return redirect(f"/login")


@app.route("/add_to_cart_from_bookmarks", methods=['post'])
def add_to_cart_from_bookmarks():
    if current_user.is_authenticated:
        good_id = request.args.get("good_id")
        db_sess = db_session.create_session()
        users_cart_products = UsersCartProducts()
        users_cart_products.user_id = current_user.id
        users_cart_products.cart_product_id = good_id
        try:
            db_sess.add(users_cart_products)
            db_sess.commit()
        except:
            pass
        return redirect(f"/bookmark")
    else:
        return redirect(f"/login")


@app.route("/add_to_cart_from_index", methods=['post'])
def add_to_cart_from_index():
    if current_user.is_authenticated:
        good_id = request.args.get("good_id")
        db_sess = db_session.create_session()
        users_cart_products = UsersCartProducts()
        users_cart_products.user_id = current_user.id
        users_cart_products.cart_product_id = good_id
        try:
            db_sess.add(users_cart_products)
            db_sess.commit()
        except:
            pass
        return redirect(f"/index")
    else:
        return redirect(f"/login")


@app.route("/add_to_bookmark_from_index", methods=['post'])
def add_to_bookmark_from_index():
    if current_user.is_authenticated:
        good_id = request.args.get("good_id")
        db_sess = db_session.create_session()
        users_products = UsersProducts()
        users_products.user_id = current_user.id
        users_products.product_id = good_id
        try:
            db_sess.add(users_products)
            db_sess.commit()
        except:
            pass
        return redirect(f"/index#popular_goods_on_index_page")
    else:
        return redirect(f"/login")


    return render_template("bookmark.html", goods=goods)


def main():
    db_session.global_init("databases/technomart.db")

    api.add_resource(products_resources.ProductsResource, '/api/products/<int:products_id>')
    api.add_resource(products_resources.ProductsListResource, '/api/products')

    api.add_resource(producers_recources.ProducersResource, '/api/producers/<int:producers_id>')
    api.add_resource(producers_recources.ProducersListResource, '/api/producers')

    app.run()


if __name__ == '__main__':
    main()
