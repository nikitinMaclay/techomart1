from flask_restful import reqparse, abort, Resource
from flask import jsonify

from . import db_session
from .producers import Producers


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)


def abort_if_producers_not_found(producers_id):
    session = db_session.create_session()
    producers = session.query(Producers).get(producers_id)
    if not producers:
        abort(404, message=f"Producers {producers_id} not found")


class ProducersResource(Resource):
    def get(self, producers_id):
        abort_if_producers_not_found(producers_id)
        session = db_session.create_session()
        producers = session.query(Producers).get(producers_id)
        return jsonify(
            {
                'producers': producers.to_dict(
                    only=('name', 'products.name', 'products.image', 'products.price', 'products.discount_price')
                )
            }
        )

    def delete(self, producers_id):
        abort_if_producers_not_found(producers_id)
        session = db_session.create_session()
        producers = session.query(Producers).get(producers_id)
        session.delete(producers)
        session.commit()
        return jsonify({'success': 'OK'})


class ProducersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        producers = session.query(Producers).all()
        return jsonify(
            {
                'producers': [
                    item.to_dict(only=(
                        'name',
                        'products.name',
                        'products.image',
                        'products.price',
                        'products.discount_price'
                    )) for item in producers
                ]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        producers = Producers(
            name=args['name']
        )
        session.add(producers)
        session.commit()
        return jsonify({'success': 'OK'})
