import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from .users_products import UsersProducts


class Products(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    producer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("producers.id"))
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    discount_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    producer = orm.relationship('Producers')

    users = relationship("User", secondary="users_products")
    cart_users = relationship("User", secondary="users_cart_products")

