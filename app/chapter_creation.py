from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.fields.core import Label, SelectMultipleField, SelectField
from wtforms.fields.simple import TextAreaField, TextField
from wtforms.validators import DataRequired, Length

class CreaChapter(FlaskForm):
    #form to create a chapter

    chapName = StringField(
        "Nom du chapitre :",
        validators = [DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )

    level = SelectMultipleField( #SelectMultipleField(
        "Niveaux",
        validators=[DataRequired(message="please select at least one")]
    )

    exos =  SelectMultipleField( #should be select multiple field 
        "Sélectionner un ou des exercises"
    )
 
   
    txt = SelectMultipleField( #test for multi select
        "Sélectionner un ou des textes à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins un texte")]
    )

    notion = SelectMultipleField(
        "Sélectionner une ou des notions à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins une notion")]
    )

    summary = TextAreaField(
        "Résumé du cours (facultatif)"
    )

    file = MultipleFileField("Choisir un fichier")


    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
