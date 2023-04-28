import sqlalchemy
from .db_session import SqlAlchemyBase


class UsersCartProducts(SqlAlchemyBase):
    __tablename__ = 'users_cart_products'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)

    cart_product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), primary_key=True)
