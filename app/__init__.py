from flask import Flask
import os

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER =  os.path.join(BASE_DIR, 'upload')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes