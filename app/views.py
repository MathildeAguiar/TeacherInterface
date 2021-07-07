from re import template
from app.session_exo import SessionExo
from app.chapter_creation import CreaChapter
import os
import random, string
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_babel import Babel #test Babel
from flask_sqlalchemy import request
from flask import Flask, render_template, url_for, redirect, request
from .forms import ResearchForm
from .creation_exo import CreaExo
from .validation import TxtBrowser


app = Flask(__name__)

#link config
app.config.from_object('config')

#more configuration for the db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

#init Bootstrap
bootstrap = Bootstrap(app)

#security 
csrf = CSRFProtect(app)

#test with Babel 

babel = Babel(app)

#imports from models (must stay here)
from app.models import MetalAnswerUser, MetalChapter, MetalExercise, MetalGroup, MetalAssignment, MetalUser, general_query2, init_db, new_exo, query_all_chaps, query_all_corpuses, query_all_sessions, query_all_exos, query_all_gram, query_all_groups, query_groups_sessions, query_groups_students, query_new_assignment, MetalNotion, query_delete_chapter, query_delete_notion, query_validation, query_exo_related_chaps, query_all_qFB, query_all_qH, query_all_qTF, query_delete_session, query_delete_exercise, query_new_chapter, query_answers_user


#routes 

#before the first request we init our db
@app.before_first_request
def before_first_request_func():
    init_db()

#test to pass the list of chapters at all templates 

@app.context_processor
def inject_chapters():
    names = list()
    side_nav_chaps = query_all_chaps()
    for c in side_nav_chaps:
        names.append(c.name)
    return dict(side_nav_chaps = names) 


#index page with the general search bar
@app.route('/')

@app.route('/form/', methods=["GET", "POST"])
def index():
    #just a test 
    #test = query_exo_related_chaps('Pronoms personnels')
    #print(test)

    form = ResearchForm()
    if form.validate_on_submit():
        return redirect(url_for('table'))
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template(
        "form.html",
        form = form,
        #template="form-template"
    )


#the general search bar's result page 
@app.route('/table/', methods=["GET", "POST"])
def table():
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
    form = CreaExo()
    #query to get all the chapters avaiable
    chaps = query_all_chaps()
    form.chap.choices = [(c.id,c.name) for c in chaps] 

    txts = query_all_corpuses()
    form.txt.choices = [(t.id, t.name) for t in txts]

    #lvls = query_all_groups()
    #form.level.choices = [(l.id, l.level) for l in lvls]

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
#@app.route('/list_exo/<chap_name>/', methods=["GET", "POST"])
@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo(): #chap_name=None
    
    chap_name = request.args.get("chapName")
    print("request args",request.args)
    print("chap name extraction", chap_name)
    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20)

    #case where we get only the exercices related to a specific chapter 

    if chap_name is not None: 
        
        exos = query_exo_related_chaps(chap_name)
        print("liste des exos returned : ", exos)

    elif chap_name is None :
        #case where we display all the exercices avaiable in the db 
        #we get the infos filled in the form 
        form = CreaExo()
        name = form.exoName.data
        #lvl = form.level.data #level.data[0] ! ici on aura potentiellement une liste et pas juste une valeur
        chaps = form.chap.data #chap.data[0] ! ici on aura potentiellement une liste et pas juste une valeur
        duration = form.tps.data
        text = form.txt.data #txt.data[0] !! ici on aura potentiellement une liste et pas juste une valeur
        questTF = form.questTF.data
        questFB = form.questFill.data
        questH = form.questHighlight.data
        tags = form.tags.data
        #addition to the db
        new_exo(name, chaps, duration, text, questTF, questFB, questH, tags)
        #print check 
        print(new_exo)

        exos = query_all_exos()


    
    return render_template(
        'list_exo.html',
        pagination = pagination,
        exos = exos
    )

@app.route('/list_exo/<exo_id>/delete_exo', methods=['POST', 'GET'])
def delete_exo(exo_id):

    query_delete_exercise(exo_id)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20)
   
    exos = query_all_exos()
    
    return render_template(
        "list_exo.html", 
        pagination = pagination,
        exos = exos
    )


@app.route('/list_exo/<exo_id>/modify_exo', methods=['GET', 'POST']) #TODO
def modify_exo(exo_id):
    exo_id = request.args.get('exo_id')
    if exo_id:
        return True
    
    return True


#page to create a new chapter
@app.route('/chapter_creation/', methods=['GET','POST'])
def chapter_creation():

    form = CreaChapter()
    #get all the levels available
    lvls = query_all_groups()
    form.level.choices = [(l.id, l.level) for l in lvls]

    #get all the exercises available 
    ex = query_all_exos()
    form.exos.choices = [(e.id, e.name) for e in ex]

    #get all the texts and notions available (for now only notions)
    notions = query_all_gram()
    form.notion.choices = [(n.id, n.name) for n in notions]

    #get all texts avaiable
    txts = query_all_corpuses()
    form.txt.choices = [(t.id, t.name) for t in txts]


    if form.validate_on_submit():      
        return redirect(url_for('new_chapter', submitted_status='True')) 
    else:
        print("Validation Failed for creation chapter")
        print(form.errors)

    return render_template(
        'chapter_creation.html',
        form = form
    )

#page where all the db's chapters are displayed 
@app.route('/list_chapters/', methods=['GET','POST'])
def list_chapters():

    """
    submitted_status = request.args.get('submitted')
    if submitted_status == 'True':
        form = CreaChapter()
        name = form.chapName.data
        levels = form.level.data
        exos = form.exos.data
        summary = form.summary.data
        tags = form.tags.data
        notionsEx = form.notion.data
        #reste à savoir si on link les textes dans la BD 
        query_new_chapter(name, levels, exos, notionsEx, summary, tags)
    """
    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
    #for now we will display all the chapters
    chaps = query_all_chaps() # we need a new query where we add the new created chapter 


    return render_template(
        'list_chapters.html',
        pagination = pagination,
        chaps = chaps
    )

@app.route('/list_chapters/<submitted_status>/new_chapter', methods=['GET','POST'])
def new_chapter(submitted_status):

    if submitted_status == 'True' :
    
        form = CreaChapter()
        name = form.chapName.data
        levels = form.level.data
        exos = form.exos.data
        summary = form.summary.data
        tags = form.tags.data
        notionsEx = form.notion.data
        #reste à savoir si on link les textes dans la BD 
        query_new_chapter(name, levels, exos, notionsEx, summary, tags)


    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
   
    chaps = query_all_chaps()
    
    return render_template(
        "list_chapters.html", 
        pagination = pagination,
        chaps = chaps
    )

@app.route('/list_chapters/<chapter_id>/delete_chapter', methods=['POST', 'GET'])
def delete_chapter(chapter_id):

    query_delete_chapter(chapter_id)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
   
    chaps = query_all_chaps()
    
    return render_template(
        "list_chapters.html", 
        pagination = pagination,
        chaps = chaps
    )


@app.route('/list_chapters/<chapter_id>/modify_chapter', methods=['GET', 'POST']) #TODO
def modify_chapter(chapter_id):
    chapter_id = request.args.get('chapter_id')
    if chapter_id:
        return True
    
    return True


#page where you have to confirm notions found by the analyser
@app.route('/validation/', methods=["GET", "POST"]) 
def validation():
    #if the submit button have been used 
    #submit_status = request.args.get("submitted")
    #print(submit_status)
    #getting the url arguments to check the vars of the query 

    notions = None
    pagination = None

    #pour éviter d'appeller des mêmes bouts de code plusieurs fois pour rien on va juste placer une condition sur le submit 
    """
    if submit_status == 'True':
        txtNameReq = request.args.get('txtName')
        #CHANGE THAT IT'S UGLY 
        page = request.args.get('page', 1, type=int)
        pagination = MetalNotion.query.paginate(page, per_page=10)
        notions = query_validation(txtNameReq)
        print("this is notions in the if ", notions)
    else : txtNameReq = None
    """

    form = TxtBrowser()
    txtName = form.txt.data

   
  
    if form.validate_on_submit():
        
        return redirect(url_for('validation_analyzed', txt_name = txtName)) # request.referrer ?    submitted_status = True,


    return render_template(
        'validation.html',
        form = form,
        notions = notions, 
        pagination = pagination,
        txtName = None,
        submit = True
    )

#??????????????????????????????????????????
@app.route('/validation/<txt_name>/analyzed/', methods=["GET", "POST"])  #<submitted_status>
def validation_analyzed(txt_name): #, submitted_status

    form = TxtBrowser()
    form_field = form.txt.data
    print(form_field)

    if txt_name:
        #txtNameReq = request.args.get('txtName')
        page = request.args.get('page', 1, type=int)
        pagination = MetalNotion.query.paginate(page, per_page=10)
        notions = query_validation(txt_name)
        print("this is notions in the if ", notions)
  
    if form.validate_on_submit and form_field:
        return redirect(url_for('validation_analyzed', txt_name = form_field))

    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )


#if we delete one notion/question from the analysis
@app.route('/validation/<notion_id>/delete_notion/', methods=["GET", "POST"]) 
def delete_validation(notion_id):

    query_delete_notion(notion_id)
    
    url_parent = request.referrer #####""???????
    print(url_parent)
    txtName = url_parent.get("txt_name")
    #print(txtName)
    #print(txtName)

    """
    return render_template(
        'validation.html',
        notions = notions, 
        pagination = pagination,
        form = form,
        txtName = txt_name,
        submit ='True'
    )
    """
    
    return redirect(url_for('validation_analyzed', txt_name=txtName))   


#if we modify a notion on the validation page
@app.route('/validation/<notion_id>/modify_notion/', methods=["GET", "POST"]) 
def modify_validation():
    return True

#connexion page 
@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
   
    return render_template(
        'connexion.html'
    )

#help page
@app.route('/help/', methods=['GET', 'POST'])
def help():
    return render_template(
        'help.html'
    )

############ Groups gestion ################

#groups page
@app.route('/groups/', methods=['GET', 'POST'])
def groups():

    page = request.args.get('page', 1, type=int)
    pagination = MetalGroup.query.paginate(page, per_page=10)

    groups = query_all_groups()

    return render_template(
        'groups.html', 
        groups = groups,
        pagination = pagination
    )

#where we can see which sessions are related to a choosen group
@app.route('/groups/<group_id>/groups_sessions', methods=['POST', 'GET'])
def groups_sessions(group_id):

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
@app.route('/groups/<group_id>/groups_students', methods=['POST', 'GET'])
def groups_students(group_id):

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
@app.route('/groups/<group_id>/groups_students/<user_id>/student', methods=['POST', 'GET'])
def student(user_id, group_id):

    student = MetalUser.query.get(user_id)
    studentFirstName = student.firstName  
    studentLastName = student.lastName

    answers = query_answers_user(user_id)  

    page = request.args.get('page', 1, type=int)
    pagination = MetalAnswerUser.query.paginate(page, per_page=20) 
   
    
    
    return render_template(
        "student.html",  
        pagination = pagination,
        studentLastName = studentLastName,
        studentFirstName = studentFirstName,
        answers = answers
    )


#exercises sessions' page
@app.route('/creation_session/',  methods=['GET', 'POST'])
def creation_session():
    
    form = SessionExo()
    #get all the levels available
    grps = query_all_groups()
    form.grps.choices = [(g.id, g.level) for g in grps]

    #get all the exercises available 
    ex = query_all_exos()
    form.exos.choices = [(e.id, e.name) for e in ex]

    #session code 
    sessionCode = "".join([random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])

     #ajouter la requete de création/ajout de la session!!!!

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

    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)
   
    sessions = query_all_sessions()

    return render_template(
        "list_sessions.html",
        pagination = pagination,
        sessions = sessions
    )

#after a new sessions has been created
@app.route('/list_sessions/<submitted_status>/new_assignment', methods=['GET','POST'])
def new_assignment(submitted_status):

    if submitted_status == 'True' :
    
        form = SessionExo()
        name = form.sessionName.data
        groups = form.grps.data
        exos = form.exos.data
        code = request.form.get("sessionCode")
        print(code)
        
        query_new_assignment(name,exos,groups, code)


    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)
   
    sessions = query_all_sessions()
    
    return render_template(
        "list_sessions.html", 
        pagination = pagination,
        sessions = sessions
    )


@app.route('/list_sessions/<session_id>/delete', methods=['POST', 'GET'])
def delete_session(session_id):

    #sess_id = request.args.get('session_id')
    #sess_id = int(sess_id)
    query_delete_session(session_id)
    

    page = request.args.get('page', 1, type=int)
    pagination = MetalAssignment.query.paginate(page, per_page=20)
   
    sessions = query_all_sessions()

    #session_id = request.args.get(session_id)
    #if session_id:

    
    return render_template(
        "list_sessions.html", 
        pagination = pagination,
        sessions = sessions
    )

    #return redirect(url_for('list_sessions'))

@app.route('/list_sessions/<session_id>/modify_session', methods=['GET', 'POST'])
def modify_session(session_id):
    session_id = request.args.get('session_id')
    if session_id:
        #edit_session(session_id) n'existe pas encore 
        return True
    
    return True

#run 
if __name__ == "__main__":
    app.run()