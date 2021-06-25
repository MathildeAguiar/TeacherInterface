from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField, Label, RadioField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

#champ dyn pattern
#     myField3 = SelectField(u'Select Account', choices=[], coerce=int) 
#acctchoices = [(c.id,c.name) for c in accounts5]             
        # form.myField3.choices = acctchoices 

class TimeLimted():
    label = "Temps limité ?"
    oui = BooleanField('oui')
    non = BooleanField('non')

class CreaExo(FlaskForm):
    #form to create an exercise

    exoName = StringField(
        "Nom de l'exercice :",
        validators=[DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )

    level = SelectMultipleField( #SelectMultipleField(
        "Niveaux",
        validators=[DataRequired(message="please select at least one")]
    )
       
    chap =  SelectMultipleField( #SelectMultipleField
        "Sélectionner un ou des chapitres"
    )

    """
    tps = RadioField(
        "Temps limité ?",
        choices= [(True, 'oui'), (False, 'non')], #changer le 'y' et faire qq chose pour permettre de choisir la durée
        validators= [DataRequired(message="Veuillez choisir une option")]
    )
    """
    tps = BooleanField(

        "Temps limité ?", 
        validators=[DataRequired(message="Veuillez choisir une option")]
    )
   
    txt = SelectMultipleField(
        "Sélectionner un ou des textes/notions à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )

    quest = SelectMultipleField(
        "Choisissez des questions",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
    )
 

    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
