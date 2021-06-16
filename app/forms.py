from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets
from wtforms.fields.core import BooleanField, SelectMultipleField, SelectField
from wtforms.validators import Length, DataRequired

l = ['All', 'Exercices', 'Chapitres', 'Questions', 'Textes']

class MultiCheckboxField(SelectMultipleField):
    #widget = widgets.TableWidget()
    widget = widgets.TableWidget()           #ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ResearchForm(FlaskForm):
    #form where we can search for elements in our database

    formContent = StringField(
        "Search ...",
        validators=[DataRequired(message="Veuillez choisir au moins un.e notion/texte"), Length(min=3, message='the query should be longer')]
    )

    category = SelectField(
        "Rechercher dans :",
        choices=l #linker ça et changer les noms 
    )
    
    cat_test = MultiCheckboxField(
        'test',
        choices=[('hi', 'hi'), ('test', 'test')]
    )
    
    #cat_test2 = BooleanField(label='Text') the label doesn't display itself
    #cat_test3 = BooleanField(label='Chapitre')
    #cat_test2 = BooleanField(label='test2' ,widget=widgets.CheckboxInput())
        
    

    submit = SubmitField('Submit')

