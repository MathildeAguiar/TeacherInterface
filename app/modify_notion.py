from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ModifyNotion(FlaskForm):
    """Form to modify a grammatical notion"""

    name = StringField( "Nom de la notion")

    notion_item = StringField("Entrez l'élément grammatical")

    submit = SubmitField('Modifier')