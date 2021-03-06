from flask.helpers import flash
from app.student_dashboard import CommentsForTeacher, CommentsToStudent
from app.modify_notion import ModifyNotion
from app.session_exo import SessionExo
from app.chapter_creation import CreaChapter
import os
import random, string
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
#from flask_babel import Babel #test Babel
from flask_sqlalchemy import request
from flask import Flask, render_template, url_for, redirect, request
from .forms import ResearchForm
from .creation_exo import CreaExo
from .validation import TxtBrowser
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np


app = Flask(__name__)

#link config
app.config.from_object('config')

#more configuration for the db, here we use sqlite as database system
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

#init Bootstrap
bootstrap = Bootstrap(app)

#security 
csrf = CSRFProtect(app)

#test with Babel 
#babel = Babel(app)

#CKEditor
ckeditor = CKEditor(app)

#imports from models (must stay here)
from app.models import MetalChapter, MetalExercise, MetalGroup, MetalAssignment, MetalUser, edit_assignment, edit_chapter, edit_exo, edit_notion, general_query2, init_db, new_exo, query_all_chaps, query_all_corpuses, query_all_sessions, query_all_exos, query_all_gram, query_all_groups, query_assignments_by_user, query_groups_sessions, query_groups_students, query_new_assignment, MetalNotion, query_delete_chapter, query_delete_notion, query_validation, query_all_qFB, query_all_qH, query_all_qTF, query_delete_session, query_delete_exercise, query_new_chapter, query_update_comment, query_validate_notion


#routes 

#before the first request we init our db
@app.before_first_request
def before_first_request_func():
    """Initialization of the database"""
    init_db()

#test to pass the list of chapters at all templates 
##### DELETE HERE 
"""@app.context_processor
def inject_chapters():
   
    #app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'
   
    names = list()
    side_nav_chaps = query_all_chaps()
    for c in side_nav_chaps:
        names.append(c.name)
    return dict(side_nav_chaps = names) 
"""




#index page with the general search bar
@app.route('/')

@app.route('/form/', methods=["GET", "POST"])
def index():
    """Index page with the general search bar"""

    form = ResearchForm()
    if form.validate_on_submit():
        return redirect(url_for('table'))
   
    return render_template(
        "form.html",
        form = form,
    )


#the general search bar's result page 
@app.route('/table/', methods=["GET", "POST"])
def table():
    """Results from a search on the index page"""
    form = ResearchForm()
    query = form.formContent.data
    category = form.category.data
    res = general_query2(query, category)

    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20) #which class to paginate from 


    return render_template(
    'table.html',
    res = res,
    pagination = pagination       
    )

#page to create a new exercice 
@app.route('/creation_exo/', methods=["GET", "POST"])
def creation_exo():
    """Form to create a new exercise"""
    form = CreaExo()
    #query to get all the chapters avaiable
    chaps = query_all_chaps()
    form.chap.choices = [(c.id,c.name) for c in chaps] 

    txts = query_all_corpuses()
    form.txt.choices = [(t.id, t.name) for t in txts]

    questsTF= query_all_qTF() 
    form.questTF.choices = [(q.id, q.instructions) for q in questsTF]

    questsFill= query_all_qFB()
    form.questFill.choices = [(q.id, q.instructions) for q in questsFill]

    questsHigh= query_all_qH()
    form.questHighlight.choices = [(q.id, q.instructions) for q in questsHigh]


    if form.validate_on_submit():
        return redirect(url_for('list_exo')) 

    return render_template(
        'creation_exo.html',
        form = form
    )

#result page from the exercice creation, displaying all the avaiable exercices
@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo(): 
    """Displaying all the avaiable exercices"""

    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20)

    #if the list of exos are displayed after a modification 
    modified = request.args.get('modified')

    if modified:
        modif_form= CreaExo()
        name = modif_form.name.data 
        chaps = modif_form.chap.data
        duration = modif_form.tps.data
        text = modif_form.txt.data 
        questTF = modif_form.questTF.data
        questFB = modif_form.questFill.data
        questH = modif_form.questHighlight.data
        tags = modif_form.tags.data
        edit_exo(modified, name, chaps, duration, text, questTF, questH, questFB, tags)

        exos = query_all_exos()


    #creation of a new chapter (not modification)
    #we get the infos filled in the form 
    form = CreaExo()
    name = form.name.data 
    chaps = form.chap.data
    duration = form.tps.data
    text = form.txt.data 
    questTF = form.questTF.data
    questFB = form.questFill.data
    questH = form.questHighlight.data
    tags = form.tags.data
    #addition to the db
    new_exo(name, chaps, duration, text, questTF, questFB, questH, tags)

    exos = query_all_exos()

    return render_template(
        'list_exo.html',
        pagination = pagination,
        exos = exos
    )

@app.route('/list_exo/<exo_id>/delete_exo/', methods=['POST', 'GET'])
def delete_exo(exo_id):
    """Displaying all the avaiable exercices, after a deletion"""


    query_delete_exercise(exo_id)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20)
   
    exos = query_all_exos()
    
    return render_template(
        "list_exo.html", 
        pagination = pagination,
        exos = exos
    )


@app.route('/list_exo/<exo_id>/modify_exo/', methods=['GET', 'POST']) #correct the query 
def modify_exo(exo_id):
    """Displaying all the avaiable exercices, after a modification"""

    if exo_id:
        exo = MetalExercise.query.get(exo_id)
        prefilled_form = CreaExo(obj=exo)

        chaps = query_all_chaps()
        prefilled_form.chap.choices = [(c.id,c.name) for c in chaps] 

        txts = query_all_corpuses()
        prefilled_form.txt.choices = [(t.id, t.name) for t in txts]

        questsTF= query_all_qTF() 
        prefilled_form.questTF.choices = [(q.id, q.instructions) for q in questsTF]

        questsFill= query_all_qFB()
        prefilled_form.questFill.choices = [(q.id, q.instructions) for q in questsFill]

        questsHigh= query_all_qH()
        prefilled_form.questHighlight.choices = [(q.id, q.instructions) for q in questsHigh]


        if prefilled_form.validate_on_submit():
            edit_exo(exo_id)
            return redirect(url_for('list_exo', modified=exo_id)) 
    
    return render_template(
        "creation_exo.html",
        form = prefilled_form,
        exo_id = exo_id,
        modify_status = True 
    )


@app.route('/chapter_creation/', methods=['GET','POST'])
def chapter_creation():
    """Page to create a new chapter"""


    form = CreaChapter()
    #get all the levels available
    lvls = query_all_groups()
    form.level.choices = [(l.id, l.level) for l in lvls]

    #get all the exercises available 
    ex = query_all_exos()
    form.exos.choices = [(e.id, e.name) for e in ex]

    #get all the notions available
    notions = query_all_gram()
    form.notion.choices = [(n.id, n.name) for n in notions]

    #get all texts avaiable
    txts = query_all_corpuses()
    form.txt.choices = [(t.id, t.name) for t in txts]


    if form.validate_on_submit():      
        return redirect(url_for('new_chapter', submitted_status='True')) 


    return render_template(
        'chapter_creation.html',
        form = form
    )


@app.route('/list_chapters/', methods=['GET','POST'])
def list_chapters():
    """Displaying all the avaiable chapters"""

    modified = request.args.get('modified')
    if modified:
        form = CreaChapter()
        name = form.name.data  
        levels = form.level.data
        exos = form.exos.data
        #txts = form.txt.data
        summary = form.summary.data
        file = form.file.data
        tags = form.tags.data
        notionsEx = form.notion.data
        cycle = form.cycle.data
        edit_chapter(modified, name, levels, cycle, exos, notionsEx, summary, file, tags) 


    
    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
    chaps = query_all_chaps() 


    return render_template(
        'list_chapters.html',
        pagination = pagination,
        chaps = chaps
    )

@app.route('/list_chapters/<submitted_status>/new_chapter/', methods=['GET','POST'])
def new_chapter(submitted_status):
    """Displaying all the avaiable chapters, after an addition"""

    if submitted_status == 'True' :
    
        form = CreaChapter()
        name = form.name.data  
        levels = form.level.data
        exos = form.exos.data
        summary = form.summary.data
        file = form.file.data
        tags = form.tags.data
        notionsEx = form.notion.data
        cycle = form.cycle.data
        query_new_chapter(name, levels, cycle, exos, notionsEx, summary, file, tags)


    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
   
    chaps = query_all_chaps()
    
    return render_template(
        "list_chapters.html", 
        pagination = pagination,
        chaps = chaps
    )

@app.route('/list_chapters/<chapter_id>/delete_chapter/', methods=['POST', 'GET'])
def delete_chapter(chapter_id):
    """Displaying all the avaiable chapters, after a deletion"""

    query_delete_chapter(chapter_id)
    
    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
   
    chaps = query_all_chaps()
    
    return render_template(
        "list_chapters.html", 
        pagination = pagination,
        chaps = chaps
    )


@app.route('/list_chapters/<chapter_id>/modify_chapter/', methods=['GET', 'POST']) 
def modify_chapter(chapter_id):
    """Displaying all the avaiable chapters, after a modification"""


    if chapter_id:
        #we query the corresponding object to the id 
        chapter = MetalChapter.query.get(chapter_id)
        prefilled_form = CreaChapter(obj=chapter)

        lvls = query_all_groups()
        prefilled_form.level.choices = [(l.id, l.level) for l in lvls]

        ex = query_all_exos()
        prefilled_form.exos.choices = [(e.id, e.name) for e in ex]

        notions = query_all_gram()
        prefilled_form.notion.choices = [(n.id, n.name) for n in notions]

        txts = query_all_corpuses()
        prefilled_form.txt.choices = [(t.id, t.name) for t in txts]
        

        if prefilled_form.validate_on_submit():
            
            return redirect(url_for('list_chapters', modified=chapter_id))

    return render_template(
        "chapter_creation.html",
        form = prefilled_form,
        modify_status = True, #variable to pass to the template to know if we are modifying or creating (see in action of <form> tag)
        chapter_id = chapter_id #on donne l'id dans les var de l'url de retour pour pouvoir traiter la requete de la modification 
    )



@app.route('/validation/', methods=["GET", "POST"]) 
def validation():
    """Page where we can analyze a text and validate or not the grammatical notions found by the analyzer"""

    notions = None
    pagination = None

    form = TxtBrowser()
    txtName = form.txt.data
  
    if form.validate_on_submit():
        
        return redirect(url_for('validation_analyzed', txt_name = txtName))


    return render_template(
        'validation.html',
        form = form,
        notions = notions, 
        pagination = pagination,
        txtName = None,
        submit = True
    )

@app.route('/validation/<txt_name>/analyzed/', methods=["GET", "POST"])  
def validation_analyzed(txt_name): 
    """Page where we can analyze a text and validate or not the grammatical notions found by the analyzer, after an analyzis"""


    form = TxtBrowser()
    form_field = form.txt.data

    modified = request.args.get('modified')

    if txt_name:
        page = request.args.get('page', 1, type=int)
        pagination = MetalNotion.query.paginate(page, per_page=30)
        notions = query_validation(txt_name)

  
    if form.validate_on_submit() and form_field:
        return redirect(url_for('validation_analyzed', txt_name = form_field))

    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )

@app.route('/validation/<txt_name>/analyzed/<notion_id>/validated', methods=["GET", "POST"])  
def validate_validation(txt_name, notion_id):
    query_validate_notion(notion_id, txt_name)

    page = request.args.get('page', 1, type=int)
    pagination = MetalNotion.query.paginate(page, per_page=30)
    notions = query_validation(txt_name)
    form = TxtBrowser()
    form_field = form.txt.data

    if form.validate_on_submit() and form_field:
        return redirect(url_for('validation_analyzed', txt_name = form_field))

    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )



@app.route('/validation/<txt_name>/analyzed/<notion_id>/deleted', methods=["GET", "POST"])  
def delete_validation(notion_id, txt_name):
    """Page where we can analyze a text and validate or not the grammatical notions found by the analyzer, after a deletion"""
    
    #query to delete the notion related to the text
    query_delete_notion(notion_id, txt_name)
    

    #usual elements and notions
    page = request.args.get('page', 1, type=int)
    pagination = MetalNotion.query.paginate(page, per_page=30)
    notions = query_validation(txt_name)
    #search bar
    form = TxtBrowser()
    form_field = form.txt.data

    if form.validate_on_submit() and form_field:
        return redirect(url_for('validation_analyzed', txt_name = form_field))

    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )


@app.route('/validation/<txt_name>/analyzed/<notion_id>/modified', methods=["GET", "POST"])  
def modified_validation(notion_id, txt_name):
    #If we modify a notion on the validation page

    modified_notion_form = ModifyNotion()
    newName = modified_notion_form.name.data
    notionIt = modified_notion_form.notion_item.data
    edit_notion(notion_id, newName, notionIt)
    
    #usual elements and notions
    page = request.args.get('page', 1, type=int)
    pagination = MetalNotion.query.paginate(page, per_page=30)
    notions = query_validation(txt_name)
    #search bar
    form = TxtBrowser()
    form_field = form.txt.data

    if form.validate_on_submit() and form_field:
        return redirect(url_for('validation_analyzed', txt_name = form_field))

   
    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )


#if we modify a notion on the validation page
@app.route('/validation/<notion_id>/modify_notion/', methods=["GET", "POST"]) 
def modify_validation(notion_id):
    #If we modify a notion on the validation page

    txt_name = request.args.get('txt_name')

    n = MetalNotion.query.get(notion_id)
    form = ModifyNotion(obj=n)
   
    if form.validate_on_submit():
        return redirect(url_for('modified_validation', txt_name=txt_name, notion_id=notion_id))


    return render_template(
        "modify_notion.html",
        form = form,
        txt_name = txt_name,
        notion_id = notion_id
    )


#connexion page 
@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
    """Connexion page"""
   
    return render_template(
        'connexion.html'
    )

#help page
@app.route('/help/', methods=['GET', 'POST'])
def help():
    """Help page"""
    return render_template(
        'help.html'
    )

############ Groups gestion ################

#groups page
@app.route('/groups/', methods=['GET', 'POST'])
def groups():
    """List of all groups page"""

    page = request.args.get('page', 1, type=int)
    pagination = MetalGroup.query.paginate(page, per_page=10)

    groups = query_all_groups()

    return render_template(
        'groups.html', 
        groups = groups,
        pagination = pagination
    )

#where we can see which sessions are related to a choosen group
@app.route('/groups/<group_id>/groups_sessions/', methods=['POST', 'GET'])
def groups_sessions(group_id):
    """List of all assignments done by 1 group"""

    sessions = query_groups_sessions(group_id) 

    grpName = MetalGroup.query.get(group_id)
    grpName = grpName.level
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalGroup.query.paginate(page, per_page=20)
   
    
    
    return render_template(
        "groups_sessions.html",  
        pagination = pagination,
        sessions = sessions,
        grpName = grpName
    )



#where we can see which students are related to a choosen group
@app.route('/groups/<group_id>/groups_students/', methods=['POST', 'GET'])
def groups_students(group_id):
    """List of all students for 1 group"""

    students = query_groups_students(group_id) 

    grpName = MetalGroup.query.get(group_id)
    grpName = grpName.level    

    page = request.args.get('page', 1, type=int)
    pagination = MetalUser.query.paginate(page, per_page=20) 
   
    
    
    return render_template(
        "groups_students.html",  
        pagination = pagination,
        students = students,
        grpName = grpName
    )


#where we can see which students are related to a choosen group
@app.route('/groups/<group_id>/groups_students/<user_id>/student/', methods=['POST', 'GET'])
def student(user_id, group_id):
    """Profile of 1 student"""

    student = MetalUser.query.get(user_id)
    studentFirstName = student.firstName  
    studentLastName = student.lastName
    comment_student = student.comment_student
    comment_teacher = student.comment_teacher

    assignments = query_assignments_by_user(user_id)  

    form_com_student = None
    form_com_teacher = None
    comment_zone =  None

    #to display the typing zone for the student comment
    if request.args.get("comment") == 'zone1':
        comment = student  #.comment_student
        form_com_student = CommentsToStudent(request.form, obj = comment)
        comment_zone = 'zone1'
    
    #to display the typing zone for the teacher comment 
    elif request.args.get("comment") == 'zone2':
        comment = student   #.comment_teacher
        form_com_teacher = CommentsForTeacher(request.form, obj=comment)
        comment_zone = 'zone2'

    #to sned the modifications of the comment zone 
    if request.args.get('submitted') == 'submitted_zone2':
        form_filled_teacher = CommentsForTeacher()
        comm = form_filled_teacher.comment_teacher.data
        query_update_comment(user_id, 'submitted_zone2', comm)
        comment_teacher = student.comment_teacher


    elif request.args.get('submitted')=='submitted_zone1':
        form_filled_student = CommentsToStudent()
        comm = form_filled_student.comment_student.data
        query_update_comment(user_id, 'submitted_zone1', comm)
        comment_student = student.comment_student

    ##### Change with the grades of the student here #########
    x = np.arange(0, 20, step=.5) #mock function to display the grades
    y = np.random.randint(2,20)    #np.sqrt(x) + np.random.randint(2,50)
    TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)")
    ]
    plot = figure(title="R??sultats",x_axis_label="Date", x_axis_type='datetime', y_axis_label="Note", toolbar_location="above",
           plot_width=1200, plot_height=500, sizing_mode="stretch_width", tooltips = TOOLTIPS)
    plot.line(x,y, line_width= 2)
    #plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))

    script, div = components(plot)
    #kwargs = {'script': script, 'div': div}
    #kwargs['title'] = 'bokeh-with-flask'    
    #return render_template('index.html', **kwargs)
    
    
    return render_template(
        "student.html",  
        studentLastName = studentLastName,
        studentFirstName = studentFirstName,
        form_com_student = form_com_student,
        form_com_teacher = form_com_teacher,
        assignments = assignments,
        group_id = group_id,
        user_id = user_id,
        comment_zone = comment_zone,
        comment_student = comment_student,
        comment_teacher = comment_teacher,
        script= script,
        div = div 
    )


########## Assignments pages #########

@app.route('/creation_session/',  methods=['GET', 'POST'])
def creation_session():
    """Page to create a new assignment"""
    
    form = SessionExo()
    #get all the levels available
    grps = query_all_groups()
    form.grps.choices = [(g.id, g.level) for g in grps]

    #get all the exercises available 
    ex = query_all_exos()
    form.exos.choices = [(e.id, e.name) for e in ex]

    #session code 
    sessionCode = "".join([random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
    form.code.description = "Entrez un code personnalis??. Ou nous vous suggerons celui-ci : " + sessionCode
    form.code.default = sessionCode


    if form.validate_on_submit():      
        return redirect(url_for('new_assignment', submitted_status=True)) 

    return render_template(
        "creation_session.html",
        form = form,
        sessionCode = sessionCode
    )

#list of all sessions created 
@app.route('/list_sessions/',  methods=['GET', 'POST'])
def list_sessions():
    """List of all assignments"""

    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)

    modified = request.args.get('modified')
    if modified:
        form = SessionExo()
        name = form.name.data
        groups = form.grps.data
        exos = form.exos.data
        edit_assignment(modified, name, groups, exos)

   
    sessions = query_all_sessions()

    return render_template(
        "list_sessions.html",
        pagination = pagination,
        sessions = sessions
    )

#after a new sessions has been created
@app.route('/list_sessions/<submitted_status>/new_assignment/', methods=['GET','POST'])
def new_assignment(submitted_status):
    """List of all assignments, after addition"""

    if submitted_status == 'True' :
    
        form = SessionExo()
        name = form.name.data
        groups = form.grps.data
        exos = form.exos.data
        code = form.code.data 
        
        query_new_assignment(name,exos,groups, code)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)
   
    sessions = query_all_sessions()
    
    return render_template(
        "list_sessions.html", 
        pagination = pagination,
        sessions = sessions
    )


@app.route('/list_sessions/<session_id>/delete/', methods=['POST', 'GET'])
def delete_session(session_id):
    """List of all assignments, after deletion"""

    query_delete_session(session_id)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)
   
    sessions = query_all_sessions()

    
    return render_template(
        "list_sessions.html", 
        pagination = pagination,
        sessions = sessions
    )


@app.route('/list_sessions/<session_id>/modify_session/', methods=['GET', 'POST'])
def modify_session(session_id):
    """List of all assignments, after modification"""

    if session_id:
        #we query the corresponding object to the id 
        assignment = MetalAssignment.query.get(session_id)
        prefilled_form = SessionExo(request.form, obj=assignment)
        
        #get all the levels available
        grps = query_all_groups()
        prefilled_form.grps.choices = [(g.id, g.level) for g in grps]
        #prefilled_form.grps.data = [s.level for s in assignment.group]

        #get all the exercises available 
        ex = query_all_exos()
        prefilled_form.exos.choices = [(e.id, e.name) for e in ex]
        
        sessCode = assignment.code

        if prefilled_form.validate_on_submit():

            return redirect(url_for('list_sessions', modified=session_id)) 


    return render_template(
        "creation_session.html",
        form = prefilled_form,
        sessionCode = sessCode, 
        session_id = session_id,
        modify_status = True #variable to pass to the template to know if we are modifying or creating (see in action of <form> tag)
    )


#run 
if __name__ == "__main__":
    app.run()