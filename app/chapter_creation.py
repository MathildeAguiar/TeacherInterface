from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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

    level = SelectField( #SelectMultipleField(
        "Niveaux",
        validators=[DataRequired(message="please select at least one")]
    )

    exos =  SelectField( #should be select multiple field 
        "Sélectionner un ou des exercises"
    )
 
   
    txt = SelectField(
        "Sélectionner un ou des textes/notions à inclure",
        validators= [DataRequired(message="Veuillez choisir au moins un.e notion/texte")]
    )


    """ 
     we can add a text zone for the teacher to enter informations about the chapter --> need to do a new field in the db 
    """

    summary = TextAreaField(
        "Résumé du cours (optionnel)"
    )




    tags = StringField(
        "Mots-clés (facultatif)"      
    )

    submit = SubmitField('Créer')
