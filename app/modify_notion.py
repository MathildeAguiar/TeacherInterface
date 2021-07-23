from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ModifyNotion(FlaskForm):
    name = StringField( "Nom de la notion")

    notion_item = StringField("Entrez l'élément grammatical")

    submit = SubmitField('Modifier')