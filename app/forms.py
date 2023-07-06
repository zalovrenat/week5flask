from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonSearch(FlaskForm):
    pokename = StringField(label='Please Enter Pokemon Name Here', validators=[DataRequired()])
    submit = SubmitField()