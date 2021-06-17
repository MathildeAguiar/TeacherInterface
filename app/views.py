import os
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_babel import Babel #test Babel
from flask_sqlalchemy import request
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

#test with Babel 

babel = Babel(app)

#imports from models (must stay here)
from app.models import MetalExercise, general_query2, init_db, new_exo, query_all_chaps, query_all_exos, query_all_gram, query_all_groups, query_all_quests, MetalChapter, MetalNotion, query_validation, query_exo_related_chaps


#routes 

#before the first request we init our db
@app.before_first_request
def before_first_request_func():
    init_db()

#test to pass the list of chapters at all templates 

@app.context_processor
def inject_chapters():
    names = list()
    chaps = query_all_chaps()
    for c in chaps:
        names.append(c.name)
    print("chaps :", chaps)
    print("names of chaps", names)
    return dict(chaps = names) 


#index page with the general search bar
@app.route('/')

@app.route('/form/', methods=["GET", "POST"])
def index():
    #just a test 
    test = query_exo_related_chaps('Pronoms personnels')
    print(test)

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
    chaps = res,
    pagination = pagination       
    )

#page to create a new exercice 
@app.route('/creation_exo/', methods=["GET", "POST"])
def creation_exo():
    form = CreaExo()
    #query to get all the chapters avaiable
    chaps = query_all_chaps()
    print(chaps)
    form.chap.choices = [(c.id,c.name) for c in chaps] #checker au debugger si on a bien ce que l'on veut mais sinon ok

    #query for all notions (should have texts also) avaiable
    notions = query_all_gram()
    form.txt.choices = [(n.id, n.name) for n in notions]

    lvls = query_all_groups()
    form.level.choices = [(l.id, l.level) for l in lvls]

    #form.tps.name = 'oui' looking for the right way to display propositions 

    #quests = query_all_quests()
    
    if form.validate_on_submit():
        return redirect(url_for('list_exo')) #change
    return render_template(
        'creation_exo.html',
        form = form
    )

#result page from the exercice creation, displaying all the avaiable exercices
@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo():
    
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
    #print(new_exo)

    #pagination
    page = request.args.get('page', 1, type=int)
    pagination = MetalExercise.query.paginate(page, per_page=20)
    exos = query_all_exos()
    
    return render_template(
        'list_exo.html',
        pagination = pagination,
        exos = exos
    )

#page where you have to confirm notions found by the analyser
#@app.route('/validation/<int:count>/', methods=["GET", "POST"])  #ou sinon on fait 2 url une avec <> et l'autre sans 
#def validation(count):
@app.route('/validation/', methods=["GET", "POST"]) 
def validation():
    count = 0
    form = TxtBrowser()
    txtName = form.txt.data
    print(txtName)
    #res_query = query_validation(txtName)

    page = request.args.get('page', 1, type=int)
    pagination = MetalNotion.query.paginate(page, per_page=10)
    notions = query_validation(txtName)
   
    #for now we will just query all the notions since we don't have our anaylyser
    """
    if count > 0:
        notions = query_all_gram()
        print(notions)
    elif count == 0:
        notions = None
    """
    if form.validate_on_submit():
        count +=1
        #count n'est pas retransmis au refresh de validation, il faudrait le return 
        
        return redirect(url_for('validation/<count>/')) # request.referrer    render_template('validation.html', form= form, notions = notions, pagination=pagination) #change
        #if we validate this we stay on the same page and we have new things that appear 
        #how to link that ???

    return render_template(
        'validation.html',
        form = form,
        notions = notions, 
        pagination = pagination,
        txtName = txtName,
        #res_query = res_query
    )
    
"""
#route if it's not the first loading 
@app.route('/validation/<int:count>/', methods=["GET", "POST"])  #ou sinon on fait 2 url une avec <> et l'autre sans 
def validation(count):

    form = TxtBrowser()
    txtName = form.txt.data

    if count > 0:
        page = request.args.get('page', 1, type=int)
        pagination = MetalNotion.query.paginate(page, per_page=10)
        notions = query_validation(txtName)
    elif count == 0:
        notions = None

    if form.validate_on_submit():
        count +=1        
        return redirect(url_for('validation/<count>/'))

    return render_template(
        'validation.html',
        form = form,
        notions = notions, 
        pagination = pagination,
        txtName = txtName
    )
"""

#connexion page 
@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
   
    return render_template(
        'connexion.html'
    )



if __name__ == "__main__":
    app.run()