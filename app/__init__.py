from flask import Flask
from .views import app
from . import models

# lien avec la base de données dans models.py
#models.db.init_app(app)
@app.cli.command()
def init_db():
    models.init_db()