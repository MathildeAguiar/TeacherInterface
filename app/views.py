import os
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import request, SQLAlchemy
from flask import Flask, render_template, url_for, redirect
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

#imports from models (must stay here)
from app.models import MetalExercise, general_query, init_db, new_exo, query_all_chaps, query_all_exos, query_all_gram, query_all_quests, MetalChapter, MetalGrammaticalElement


#routes 

#before the first request we init our db
@app.before_first_request
def before_first_request_func():
    init_db()

#index page with the general search bar
@app.route('/')

@app.route('/form/', methods=["GET", "POST"])
def index():
    form = ResearchForm()
    if form.validate_on_submit():
        return redirect(url_for('table'))
    return render_template(
        "form.html",
        form = form,
        template="form-template"
    )


#the general search bar's result page 
@app.route('/table/', methods=["GET", "POST"])
def table():
    #form = ResearchForm()
    #query = form.formContent.data
    page = request.args.get('page', 1, type=int)
    #chaps = query_all_chaps()
    #pagination = MetalChapter.query.paginate(page, per_page=10)
    chaps = query_all_exos()
    #chaps = general_query(query)
    pagination = MetalExercise.query.paginate(page, per_page=5)


    return render_template(
    'table.html',
    chaps = chaps,
    pagination = pagination       
    )

#page to create a new exercice 
@app.route('/creation_exo/', methods=["GET", "POST"])
def creation_exo():
    form = CreaExo()
    #chaps = MetalChapter.query.filter_by(MetalChapter.name).all()
    #notions = MetalGrammaticalElement.query.filter_by(MetalGrammaticalElement.name).all()
    #quests = MetalQuestion.query.filter_by(MetalQuestion.instructions).all()
    #notions = query_all_gram()
    #quests = query_all_quests()
    #chaps = query_all_chaps()
    if form.validate_on_submit():
        return redirect(url_for('list_exo')) #change
    return render_template(
        'creation_exo.html',
        form = form
        #notions = notions,
        #chaps = chaps, 
        #quests = quests
    )

#result page from the exercice creation, displaying all the avaiable exercices
@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo():
    
    #chaps = pagination.items
    #print(chaps)
    #change the names 
    
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

    #pagination
    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=30)
    exos = query_all_exos()
    
    return render_template(
        'list_exo.html',
        pagination = pagination,
        exos = exos
        #chaps = chaps
    )

#page where you have to confirm notions found by the analyser
@app.route('/validation/', methods=["GET", "POST"]) 
def validation():
    form = TxtBrowser()
    txtName = form.txt.data
    #for now we will just query all the notions since we don't have our anaylyser
    notions = query_all_gram()
    page = request.args.get('page', 1, type=int)
    pagination = MetalGrammaticalElement.query.paginate(page, per_page=10)

    if form.validate_on_submit():
        return redirect(url_for('validation')) #change
        #if we validate this we stay on the same page and we have new things that appear 
        #how to link that ???

    return render_template(
        'validation.html',
        form = form,
        #for the table 
        notions = notions, 
        #titles = titles
        pagination = pagination,
        txtName = txtName
    )

#connexion page 
@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
   
    return render_template(
        'connexion.html'
    )



if __name__ == "__main__":
    app.run()