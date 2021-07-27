from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
#for the comments 
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField

"""
plot = figure()
plot.circle([1,2], [3,4])

html = file_html(plot, CDN, "my plot")
"""

class CommentsToStudent(FlaskForm): #comments that'll be viewable but the student 
    comment_student = CKEditorField("Commentaires pour l'élève") 

    submit = SubmitField('Envoyer')

class CommentsForTeacher(FlaskForm): #comments that the teacher can save avout the student but only viewable by him.herself

    comment_teacher = CKEditorField("Commentaires personnels sur l'élève (non visibles par ce dernier)")

    submit = SubmitField('Valider')
