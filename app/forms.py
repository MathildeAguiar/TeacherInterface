from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets
from wtforms.fields.core import BooleanField, SelectMultipleField, SelectField
from wtforms.validators import Length

l = ['None', 'Exercices', 'Chapitres', 'Questions']

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ResearchForm(FlaskForm):
    #form where we can search for elements in our database

    formContent = StringField(
        "Search ...",
        validators=[Length(min=3, message='the query should be longer')]
    )

    category = SelectField(
        "Rechercher dans :",
        choices=l #linker ça et changer les noms 
    )
    """
    cat_test = MultiCheckboxField(
        'test',
        choices=[('hi', 'h'), ('honk', 'honk')]
    )
    """
    #cat_test2 = BooleanField(label='test2' ,widget=widgets.CheckboxInput())
        
    

    submit = SubmitField('Submit')

