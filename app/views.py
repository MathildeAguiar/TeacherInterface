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
from app.models import MetalChapter, MetalExercise, MetalGroup, MetalAssignment, general_query2, init_db, new_exo, query_all_chaps, query_all_corpuses, query_all_sessions, query_all_exos, query_all_gram, query_all_groups, query_all_quests, MetalNotion, query_validation, query_exo_related_chaps, query_all_qFB, query_all_qH, query_all_qTF


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

    lvls = query_all_groups()
    form.level.choices = [(l.id, l.level) for l in lvls]

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
        print("liste des exos rreturned : ", exos)

    elif chap_name is None :
        #case where we display all the exercices avaiable in the db 
        #we get the infos filled in the form 
        form = CreaExo()
        name = form.exoName.data
        lvl = form.level.data #level.data[0] ! ici on aura potentiellement une liste et pas juste une valeur
        chapId = form.chap.data #chap.data[0] ! ici on aura potentiellement une liste et pas juste une valeur
        duration = form.tps.data
        text = form.txt.data #txt.data[0] !! ici on aura potentiellement une liste et pas juste une valeur
        quest = form.quest.data
        tags = form.tags.data
        #addition to the db
        new_exo(name, lvl, chapId, duration, text, quest, tags)
        #print check 
        print(new_exo)

        exos = query_all_exos()


    
    return render_template(
        'list_exo.html',
        pagination = pagination,
        exos = exos
    )


#page to create a new chapter
@app.route('/chapter_creation', methods=['GET','POST'])
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

    #ajouter la requete de création/ajout du chap!!!!

    return render_template(
        'chapter_creation.html',
        form = form
    )

#page where all the db's chapters are displayed 
@app.route('/list_chapters/', methods=['GET','POST'])
def list_chapters():

    page = request.args.get('page', 1, type=int)
    pagination = MetalChapter.query.paginate(page, per_page=20)
    #for now we will display all the chapters
    chaps = query_all_chaps() # we need a new query where we add the new created chapter 


    return render_template(
        'list_chapters.html',
        pagination = pagination,
        chaps = chaps
    )



#page where you have to confirm notions found by the analyser
#@app.route('/validation/<int:count>/', methods=["GET", "POST"])  #ou sinon on fait 2 url une avec <> et l'autre sans 
#def validation(count):
@app.route('/validation/', methods=["GET", "POST"]) 
def validation():
    #if the submit button have been used 
    submit_status = request.args.get("submitted")
    print(submit_status)
    #getting the url arguments to check the vars of the query 

    notions = None
    pagination = None

    #pour éviter d'appeller des mêmes bouts de code plusieurs fois pour rien on va juste placer une condition sur le submit 

    if submit_status == 'True':
        txtNameReq = request.args.get('txtName')
        #CHANGE THAT IT'S UGLY 
        page = request.args.get('page', 1, type=int)
        pagination = MetalNotion.query.paginate(page, per_page=10)
        notions = query_validation(txtNameReq)
        print("this is notions in the if ", notions)
    else : txtNameReq = None


    form = TxtBrowser()
    txtName = form.txt.data

    """ moved in the if, please CLEAN THE CODE 
    page = request.args.get('page', 1, type=int)
    pagination = MetalNotion.query.paginate(page, per_page=10)
    notions = query_validation(txtName)
    """
   
  
    if form.validate_on_submit():
        
        return redirect(url_for('validation', submitted = True, txtName = txtName)) # request.referrer ?   


    return render_template(
        'validation.html',
        form = form,
        notions = notions, 
        pagination = pagination,
        txtName = txtNameReq,
        submit = submit_status
    )

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

#exercices sessions' page
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
        return redirect(url_for('list_sessions')) 

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

#run 
if __name__ == "__main__":
    app.run()