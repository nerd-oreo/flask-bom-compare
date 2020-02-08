from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from app import app
from app.utils import allowed_file, map_header_to_letter
from app.bom import Bom
import os

BOM = dict()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file_a = request.files['file_a']
        file_b = request.files['file_b']
        bom_a = Bom()
        bom_b = Bom()

        if allowed_file(file_a.filename) and allowed_file(file_b.filename):
            bom_a.filename = secure_filename(file_a.filename)
            bom_b.filename = secure_filename(file_b.filename)
            bom_a.file_path = os.path.join(app.config['UPLOAD_FOLDER'], bom_a.filename)
            bom_b.file_path = os.path.join(app.config['UPLOAD_FOLDER'], bom_b.filename)
            file_a.save(bom_a.file_path)
            file_b.save(bom_b.file_path)
            BOM['A'] = bom_a; BOM['B'] = bom_b
            return redirect(url_for('mapping'))
        else:
            flash('File extension is not allowed.')
            return redirect(url_for('home'))
    return render_template('home.html')


@app.route('/mapping')
def mapping():
    BOM['A'].header_list = map_header_to_letter(BOM['A'].file_path)
    BOM['B'].header_list = map_header_to_letter(BOM['B'].file_path)
    print(BOM['A'].header_list)
    return render_template('mapping.html', BOM=BOM)
