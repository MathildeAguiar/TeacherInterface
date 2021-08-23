from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import IntegerRangeField


class CreaExo(FlaskForm):
    """Form to create an exercise"""

    name = StringField( 
        "Nom de l'exercice :",
        validators=[DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )
    
    chap =  SelectMultipleField(
        "Sélectionner un ou des chapitres"
    )

    tps = IntegerRangeField('Temps imparti (en minutes)', default=0)
   
    txt = SelectMultipleField(
        "Sélectionner un ou des textes à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins un texte")]
    )

    questTF = SelectMultipleField(
        "Choisissez des questions de type 'Vrai ou Faux' ",
        validators=[DataRequired(message="Veuillez choisir au moins une question")] #enlever les data requiered mais il faut quand même choisir au moins 1 question !
    )

    questFill = SelectMultipleField(
        "Choisissez des questions de type 'texte à trous' ",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
    )

    questHighlight = SelectMultipleField(
        "Choisissez des questions de type 'surlignage' ",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
    )
 
    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
