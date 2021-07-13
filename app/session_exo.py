from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectMultipleField
from wtforms.validators import DataRequired, Length

class SessionExo(FlaskForm):

    name = StringField( #sessionName
        "Nom de la session d'exercices :",
        validators=[DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )

    exos = SelectMultipleField(
        "Sélectionner un ou plusieurs exercices :",
        validators=[DataRequired()]
    )

    grps = SelectMultipleField(
       "Sélectionner un ou plusieurs groupes :",
       validators= [DataRequired()]
    ) 

    submit = SubmitField('Valider')


  