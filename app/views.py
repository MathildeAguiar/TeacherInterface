from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, redirect
from .forms import ResearchForm
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

if __name__ == "__main__":
    app.run()