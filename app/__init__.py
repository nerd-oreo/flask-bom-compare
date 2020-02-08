from flask import Flask
import os

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')
SECRET_KEY = '97bee636afa8898bf16d411b5c9970c7f23d886295014487b3582870f7eafa5aaf2045845220abbc1b2a24a58b0a48817e35906327fcb90a2287da4d7a0b8064'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes
