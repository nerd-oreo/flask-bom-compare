import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app\\upload')
    SECRET_KEY = '97bee636afa8898bf16d411b5c9970c7f23d886295014487b3582870f7eafa5aaf2045845220abbc1b2a24a58b0a48817e35906327fcb90a2287da4d7a0b8064'
    
    # DB 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False