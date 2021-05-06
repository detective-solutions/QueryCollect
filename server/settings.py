# import standard modules
import os

# import third party modules
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from server.models import db, FreeQuery

# import project related modules

# create a app instance
app = Flask(__name__)

# load .env file
load_dotenv()

# set folder paths
STATIC_FOLDER = os.path.join('static', 'images')
DATA_FOLDER = os.path.join('static', 'data')

# set app configurations
app.config['IMAGES'] = STATIC_FOLDER
app.config['DATA'] = DATA_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up data base for the app instance
db.init_app(app)
app.app_context().push()
db.create_all()
migrate = Migrate(app, db)