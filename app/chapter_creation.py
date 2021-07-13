from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.fields.core import SelectMultipleField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class CreaChapter(FlaskForm):
    #form to create a chapter

    name = StringField( #chapName
        "Nom du chapitre :",
        validators = [DataRequired(message="please type a name"),
            Length(min=1, message='the name should be longer')]
    )

    level = SelectMultipleField( 
        "Niveaux",
        validators=[DataRequired(message="please select at least one")]
    )

    cycle = SelectField(
        "Choisir un cycle (facultatif)",
        choices=[('cycle1','cycle 1'), ('cycle2', 'cycle 2'), ('cycle3', 'cycle 3'), ('cycle4', 'cycle 4')]
    )

    exos =  SelectMultipleField( 
        "Sélectionner un ou des exercises"
    )
 
   
    txt = SelectMultipleField( 
        "Sélectionner un ou des textes à inclure"
        #validators= [DataRequired(message="Veuillez choisir au moins un texte")]
    )

    notion = SelectMultipleField(
        "Sélectionner une ou des notions à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins une notion")]
    )

    """
    summary = TextAreaField(
        "Résumé du cours (facultatif)"
    )
    """
    
    summary = CKEditorField('Résumé du cours (facultatif)')  # rich test area 

    file = MultipleFileField("Choisir un fichier")


    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
