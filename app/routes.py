from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from app import app
from app.utils import allowed_file, map_header_to_letter, get_worksheet_choices
from app.forms import SelectSheetForm, MappingHeaderForm
from app.bom import Bom
import os

BOM = dict()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
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
            BOM['A'] = bom_a
            BOM['B'] = bom_b
            return redirect(url_for('select_sheet'))
        else:
            flash('File extension is not allowed.')
            return redirect(url_for('upload'))
    return render_template('upload.html')


@app.route('/select_sheet', methods=['GET', 'POST'])
def select_sheet():
    try:
        form = SelectSheetForm()
        form.select_sheet_a.choices = get_worksheet_choices(BOM['A'].file_path)
        form.select_sheet_b.choices = get_worksheet_choices(BOM['B'].file_path)
        if form.validate_on_submit():
            BOM['A'].sheet_name = form.select_sheet_a.data
            BOM['B'].sheet_name = form.select_sheet_b.data
            return redirect(url_for('mapping'))
        return render_template('select_sheet.html', form=form)
    except KeyError:
        return redirect(url_for('upload'))


@app.route('/mapping', methods=['GET', 'POST'])
def mapping():
    try:
        form = MappingHeaderForm()
        choices_a = map_header_to_letter(BOM['A'].file_path, BOM['A'].sheet_name)
        choices_b = map_header_to_letter(BOM['B'].file_path, BOM['B'].sheet_name)

        form.select_col_level_a.choices = choices_a
        form.select_col_number_a.choices = choices_a
        form.select_col_desc_a.choices = choices_a
        form.select_col_rev_a.choices = choices_a
        form.select_col_qty_a.choices = choices_a
        form.select_col_ref_des_a.choices = choices_a
        form.select_col_mfg_name_a.choices = choices_a
        form.select_col_mfg_number_a.choices = choices_a

        form.select_col_level_b.choices = choices_b
        form.select_col_number_b.choices = choices_b
        form.select_col_desc_b.choices = choices_b
        form.select_col_rev_b.choices = choices_b
        form.select_col_qty_b.choices = choices_b
        form.select_col_ref_des_b.choices = choices_b
        form.select_col_mfg_name_b.choices = choices_b
        form.select_col_mfg_number_b.choices = choices_b

        if form.validate_on_submit():
            pass

        return render_template('mapping.html', form=form)
    except KeyError:
        return redirect(url_for('upload'))