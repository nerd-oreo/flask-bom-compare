from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from app import app

import os


ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file_a' not in request.files or 'file_b' not in request.files:
            flash('No files selected')
            return redirect(url_for('home'))
        file_a = request.files['file_a']
        file_b = request.files['file_b']
        
        if file_a.filename == '' or file_b.filename == '':
            flash('No files selected')
            return redirect(url_for('home'))
            
        if allowed_file(file_a.filename) and allowed_file(file_b.filename):
            filename_a = secure_filename(file_a.filename)
            filename_b = secure_filename(file_b.filename)
            file_a.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_a))
            file_b.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_b))
            return redirect(url_for('config'))
        else:
            flash('File extension is not allowed.')
            return redirect(url_for('home')) 
    return render_template('home.html')
    
@app.route('/config')
def config():
    return "Config page"