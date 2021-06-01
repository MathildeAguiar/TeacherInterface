from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class ResearchForm(FlaskForm):
    #form where we can search for elements in our database

    formContent = StringField(
        "Search ...",
        [Length(min=1, message='the query should be longer')]
    )

    submit = SubmitField('Submit')

