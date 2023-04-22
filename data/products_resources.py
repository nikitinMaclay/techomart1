from flask_restful import reqparse, abort, Resource
from flask import jsonify

from . import db_session
from .products import Products


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('producer_id', required=True, type=int)
parser.add_argument('image', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('discount_price', required=True, type=int)


def abort_if_products_not_found(products_id):
    session = db_session.create_session()
    products = session.query(Products).get(products_id)
    if not products:
        abort(404, message=f"Products {products_id} not found")


class ProductsResource(Resource):
    def get(self, products_id):
        abort_if_products_not_found(products_id)
        session = db_session.create_session()
        news = session.query(Products).get(products_id)
        return jsonify(
            {
                'products': news.to_dict(
                    only=('name', 'producer', 'image', 'price', 'discount_price')
                )
            }
        )

    def delete(self, products_id):
        abort_if_products_not_found(products_id)
        session = db_session.create_session()
        products = session.query(Products).get(products_id)
        session.delete(products)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Products).all()
        return jsonify(
            {
                'products': [
                    item.to_dict(
                        only=('name', 'producer', 'image', 'price', 'discount_price')
                    ) for item in news
                ]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        products = Products(
            name=args['name'],
            producer_id=args['producer_id'],
            image=args['image'],
            price=args['price'],
            discount_price=args['discount_price']
        )
        session.add(products)
        session.commit()
        return jsonify({'success': 'OK'})
