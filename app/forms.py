from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets
from wtforms.fields.core import SelectMultipleField, SelectField
from wtforms.validators import Length, DataRequired

l = ['All', 'Exercices', 'Chapitres', 'Questions', 'Textes', 'Notions']

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()          
    option_widget = widgets.CheckboxInput()


class ResearchForm(FlaskForm):
    """form where we can search for elements in our database, Home Page"""

    formContent = StringField(
        "Recherche ...",
        validators=[DataRequired(message="Veuillez choisir au moins un.e notion/texte"), Length(min=1, message='the query should be longer')]
    )

    category = SelectField(
        "Rechercher dans :",
        choices=l 
    )
    


    submit = SubmitField('Submit')

