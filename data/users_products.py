import sqlalchemy
from .db_session import SqlAlchemyBase


class UsersProducts(SqlAlchemyBase):
    __tablename__ = 'users_products'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)

    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), primary_key=True)
