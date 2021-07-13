from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField, IntegerField, Label, RadioField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import IntegerRangeField

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

    name = StringField( #exoName
        "Nom de l'exercice :",
        validators=[DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )
    """
    level = SelectMultipleField( #SelectMultipleField(
        "Niveaux",
        validators=[DataRequired(message="please select at least one")]
    )
    """
    
    chap =  SelectMultipleField(
        "Sélectionner un ou des chapitres"
    )

    """
    tps = RadioField(
        "Temps limité ?",
        choices= [(True, 'oui'), (False, 'non')], #changer le 'y' et faire qq chose pour permettre de choisir la durée
        validators= [DataRequired(message="Veuillez choisir une option")]
    )

    tps = BooleanField(

        "Temps limité ?", 
        validators=[DataRequired(message="Veuillez choisir une option")]
    )
    
    
    tps = IntegerField(
        "Temps limité ? Entrez une valeur en minutes"
    )
    """

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
