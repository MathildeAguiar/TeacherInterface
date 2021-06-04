from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class CreaExo(FlaskForm):
    #form to create an exercise

    exoName = StringField(
        "Nom de l'exercice :",
        [Length(min=1, message='the name should be longer')]
    )

    level = SelectMultipleField(
        "Niveaux",
        choices=[
            ('2nde', '2nde'),
            ('1e', '1ère'),
            ('term', 'Terminale'), 
            ('1A', '1A')
        ],
        validators=[DataRequired(message="please select at least one")]

    )

    chap = SelectMultipleField(
        "Sélectionner un ou des chapitres",
        choices=[                       #change with something dynamic (need the db)
            ('chap1', 'chapitre 1'),
            ("chap2", "chapitre 2")
        ]
    )

    tps = RadioField(
        "Temps limité ?",
        choices= [('y', 'oui'), ('n', 'non')],
        validators= [DataRequired(message="Veuillez choisir une option")]
    )

    txt = SelectMultipleField(
        "Sélectionner un ou des textes/notions à inclure",
        choices=[                       #change with something dynamic (need the db)
            ('txt1', 'texte 1'),
            ("txt2", "texte 2")
        ],
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )

    txt2 = StringField(
        "Sélectionner un ou des textes/notions à inclure - test 2",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )

    quest = StringField(
        "Choisissez des questions",
        validators=[DataRequired(message="Veuillez choisir au moins une question")]
    )

    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
