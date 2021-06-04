#import os 

SECRET_KEY = "H#+/3gRH_rb.Ka8Q%b!Z1561"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

