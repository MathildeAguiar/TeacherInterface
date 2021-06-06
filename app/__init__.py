from flask import Flask
from .views import app
from . import models

# lien avec la base de données dans models.py
#models.Base.init_app(app) #peut être changer models par views ici (mais garder le code dabs models)
"""
views.Base.init_app(app)
@app.cli.command()
def init_db():
    models.init_db()
    #views.init_db()
"""