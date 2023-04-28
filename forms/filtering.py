from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField


class FilteringForm(FlaskForm):
    price_from = IntegerField('min-price')
    price_to = IntegerField('max-price')
    bosch_producer = BooleanField('BOSCH')
    interscol_producer = BooleanField('ИНТЕРСКОЛ')
    makita_producer = BooleanField('MAKITA')
    dewalt_producer = BooleanField('DEWALT')
    HITACHI_producer = BooleanField('HITACHI')
    submit = SubmitField('Показать')
