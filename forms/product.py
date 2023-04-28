from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product = StringField('Поиск:', validators=[DataRequired()])
    submit = SubmitField('А')
