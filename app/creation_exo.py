from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import RadioField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

#champ dyn pattern
#     myField3 = SelectField(u'Select Account', choices=[], coerce=int) 
#acctchoices = [(c.id,c.name) for c in accounts5]             
        # form.myField3.choices = acctchoices 



class CreaExo(FlaskForm):
    #form to create an exercise

    exoName = StringField(
        "Nom de l'exercice :",
        validators=[DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )

    level = SelectField( #SelectMultipleField(
        "Niveaux",
        choices=[
            ('2nde', '2nde'),
            ('1e', '1ère'),
            ('term', 'Terminale'), 
            ('1A', '1A')
        ],
        validators=[DataRequired(message="please select at least one")]

    )
    """
    #I want to have dynamic choices 
    chap =  SelectField( #SelectMultipleField(
        "Sélectionner un ou des chapitres",
        
        choices=[                       #change with something dynamic (need the db)
            ('chap1', 'chapitre 1'),
            ("chap2", "chapitre 2")
        ]
        #choices=[chaps]
    )
    """

    chap =  SelectField(
        "Sélectionner un ou des chapitres"
    )

    tps = RadioField(
        "Temps limité ?",
        choices= [('y', 'oui'), (0, 'non')], #changer le 'y' et faire qq chose pour permettre de choisir la durée
        validators= [DataRequired(message="Veuillez choisir une option")]
    )
    """
    txt = SelectField(  #SelectMultipleField(
        "Sélectionner un ou des textes/notions à inclure",
        choices=[                       #change with something dynamic (need the db)
            ('txt1', 'texte 1'),
            ("txt2", "texte 2")
        ], #choices=[notions]
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )
    """
    txt = SelectField(
        "Sélectionner un ou des textes/notions à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )

    """ dont like it
    txt2 = StringField(
        "Sélectionner un ou des textes/notions à inclure - test 2",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )
    """
    quest = StringField(
        "Choisissez des questions",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
    )
    """ to test
    quest = SelectMultipleField(
        "Choisissez des questions",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
        #choices=[quests]
    )
    """

    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
