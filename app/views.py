import os
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import request, SQLAlchemy
from flask import Flask, render_template, url_for, redirect
from .forms import ResearchForm
from .creation_exo import CreaExo
from .validation import TxtBrowser
#from .models import MetalGrammaticalElement, MetalChapter, MetalQuestion
#import models.MetalGrammaticalElement
#from . import models
###########################################################
#from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, Table, Text, text
#from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TEXT, TINYINT, VARCHAR
#import logging as lg
###########################################################

app = Flask(__name__)

#link config
app.config.from_object('config')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')


#init Bootstrap
bootstrap = Bootstrap(app)

#############################################

#les imports depuis model se font ici (et pas avant)
from app.models import init_db, query_all_chaps


#routes 

@app.before_first_request
def before_first_request_func():
    init_db()


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


@app.route('/table/', methods=["GET", "POST"])
def table():
    #init_db()
    return render_template(
    'table.html'       
    )


@app.route('/creation_exo/', methods=["GET", "POST"])
def creation_exo():
    form = CreaExo()
    #chaps = MetalChapter() I don't think that we have to create a new object 
    #chaps = MetalChapter.query.filter_by(MetalChapter.name).all()
    #notions = MetalGrammaticalElement.query.filter_by(MetalGrammaticalElement.name).all()
    #quests = MetalQuestion.query.filter_by(MetalQuestion.instructions).all()
    if form.validate_on_submit():
        return redirect(url_for('list_exo')) #change
    return render_template(
        'creation_exo.html',
        form = form
        #notions = notions,
        #chaps = chaps, 
        #quests = quests
    )

@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo():
    #page = request.args.get('page', 1, type=int)
    #pagination = models.MetalChapter.query.paginate(page, per_page=30)
    #chaps = pagination.items
    #print(chaps)
    #change the names 
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'), ('create_time', 'Create Time')]
    return render_template(
        'list_exo.html',
        #chaps = chaps,
        titles = titles
    )

@app.route('/validation/', methods=["GET", "POST"]) #<notion_name>
def validation():
    form = TxtBrowser()

    #notions = Notion()
    #titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'), ('create_time', 'Create Time')]
    
    #pagination (need SQLAlchemy)
    #page = request.args.get('page', 1, type=int)
    #pagination = models.MetalGrammaticalElement.query.paginate(page, per_page=30)
    #notions = pagination.items
    #notions = MetalGrammaticalElement.query.filter_by(name=notion_name).all() #we need a way to get the name taped in the form


    #if form.validate_on_submit():
        #return redirect(url_for('va')) #change
        #if we validate this we stay on the same page and we have new things that appear 
        #how to link that ???

    return render_template(
        'validation.html',
        form = form,
        #for the table 
        #notions = notions, 
        #titles = titles
        #pagination = pagination
    )

@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
   
    return render_template(
        'connexion.html'
    )



if __name__ == "__main__":
    app.run()