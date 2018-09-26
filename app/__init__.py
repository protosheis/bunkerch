import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
