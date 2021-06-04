from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, redirect
from .forms import ResearchForm
from .creation_exo import CreaExo
from .validation import TxtBrowser
from .notions import Notion
#from .models import select_exo, select_student, create_connection, select_notion


app = Flask(__name__)

#init Bootstrap
bootstrap = Bootstrap(app)

#link config
app.config.from_object('config')

#routes 
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

    return render_template(
    'table.html'       
    )


@app.route('/creation_exo/', methods=["GET", "POST"])
def creation_exo():
    form = CreaExo()
    if form.validate_on_submit():
        return redirect(url_for('list_exo')) #change
    return render_template(
        'creation_exo.html',
        form = form
    )

@app.route('/list_exo/', methods=["GET", "POST"])
def list_exo():
   
    return render_template(
        'list_exo.html'
    )

@app.route('/validation/', methods=["GET", "POST"])
def validation():
    form = TxtBrowser()
    notions = Notion()
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'), ('create_time', 'Create Time')]
    
    #pagination (need SQLAlchemy)
    #page = request.args.get('page', 1, type=int)
    #pagination = Message.query.paginate(page, per_page=30)
    #notions = pagination.items

    #if form.validate_on_submit():
        #return redirect(url_for('va')) #change
        #if we validate this we stay on the same page and we have new things that appear 
        #how to link that ???

    return render_template(
        'validation.html',
        form = form,
        #for the table 
        notions = notions, 
        titles = titles
        #pagination = pagination
    )

@app.route('/connexion/', methods=["GET", "POST"])
def connexion():
   
    return render_template(
        'connexion.html'
    )



if __name__ == "__main__":
    app.run()