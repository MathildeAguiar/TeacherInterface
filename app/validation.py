from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class TxtBrowser(FlaskForm):
    #form to create an exercise

    txt = StringField(
        "Texte",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte"), Length(min=1, message="veuillez entrer un plus long titre")]
    )

    submit = SubmitField('Chercher')