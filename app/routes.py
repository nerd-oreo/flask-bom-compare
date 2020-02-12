from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from app import app, db
from app.utils import allowed_file, map_header_to_letter, get_worksheet_choices
from app.forms import SelectSheetForm, MappingHeaderForm, NewProfileForm
from app.bom import Bom
from app.profile import Profile
from app.models import Profile as mProfile
import os

BOM = dict()


@app.route('/', methods=['GET', 'POST'])
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
        form.select_col_ref_des_delimiter_a.choices = [('COMMA', 'COMMA'), ('SPACE', 'SPACE')]
        form.select_col_mfg_name_a.choices = choices_a
        form.select_col_mfg_number_a.choices = choices_a
        
        form.select_col_level_b.choices = choices_b
        form.select_col_number_b.choices = choices_b
        form.select_col_desc_b.choices = choices_b
        form.select_col_rev_b.choices = choices_b
        form.select_col_qty_b.choices = choices_b
        form.select_col_ref_des_b.choices = choices_b
        form.select_col_ref_des_delimiter_b.choices = [('COMMA', 'COMMA'), ('SPACE', 'SPACE')]
        form.select_col_mfg_name_b.choices = choices_b
        form.select_col_mfg_number_b.choices = choices_b

        if form.validate_on_submit():
            level = form.select_col_level_a.data
            number = form.select_col_number_a.data
            description = form.select_col_desc_a.data
            rev = form.select_col_rev_a.data
            qty = form.select_col_qty_a.data
            ref_des = form.select_col_ref_des_a.data
            ref_des_delimiter = form.select_col_ref_des_delimiter_a.data
            mfg_name = form.select_col_mfg_name_a.data
            mfg_number = form.select_col_mfg_number_a.data
            
            BOM['A'].set_header_list(level, number, description, rev, qty, ref_des, ref_des_delimiter, mfg_name, mfg_number)

            level = form.select_col_level_b.data
            number = form.select_col_number_b.data
            description = form.select_col_desc_b.data
            rev = form.select_col_rev_b.data
            qty = form.select_col_qty_b.data
            ref_des = form.select_col_ref_des_b.data
            ref_des_delimiter = form.select_col_ref_des_delimiter_b.data
            mfg_name = form.select_col_mfg_name_b.data
            mfg_number = form.select_col_mfg_number_b.data
            BOM['B'].set_header_list(level, number, description, rev, qty, ref_des, ref_des_delimiter, mfg_name, mfg_number)

            BOM['A'].load_excel()
            BOM['B'].load_excel()

            return redirect(url_for('profile_processing'))
        return render_template('mapping.html', form=form)
    except KeyError:
        return redirect(url_for('upload'))


@app.route('/profile/manage')
def profile_manage():
    profiles = mProfile.query.all()
    return render_template('profile_manage.html', profiles=profiles)


@app.route('/profile/add', methods=['GET', 'POST'])
def profile_add():
    form = NewProfileForm()
    if form.validate_on_submit():
        name = form.name.data
        type = form.type.data
        prefix = form.prefix.data
        suffix = form.suffix.data
        delimiter = form.delimiter.data
        action = form.action.data
        sample = form.sample.data
        profile = mProfile(name=name, type=type, prefix=prefix, suffix=suffix, delimiter=delimiter, action=action, sample=sample)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('profile_manage'))
    return render_template('profile_add.html', form=form)


@app.route('/profile/modify/<id>', methods=['GET','POST'])
def profile_modify(id):
    profile = mProfile.query.filter_by(id=id).first()
    form = NewProfileForm()
    if form.validate_on_submit():
        profile.name = form.name.data
        profile.type = form.type.data
        profile.prefix = form.prefix.data
        profile.suffix = form.suffix.data
        profile.delimiter = form.delimiter.data
        profile.action = form.action.data
        profile.sample = form.sample.data
        db.session.commit()
        return redirect(url_for('profile_manage'))
    elif request.method == 'GET':
        form.name.data = profile.name
        form.type.data = profile.type
        form.prefix.data = profile.prefix
        form.suffix.data = profile.suffix
        form.delimiter.data = profile.delimiter
        form.action.data  = profile.action
        form.sample.data = profile.sample
    return render_template('profile_modify.html', form=form)


@app.route('/profile/delete/<id>')
def profile_delete(id):
    profile = mProfile.query.filter_by(id=id).first()
    db.session.delete(profile)
    db.session.commit()
    return redirect(url_for('profile_manage'))


@app.route('/profile/processing', methods=['GET', 'POST'])
def profile_processing():
    '''
    profile = Profile()
    profile.set_profile('LP_make', 'parent', 'LFLIEP', '/', '-', 'add', '0800-OPS1-MDF')
    BOM['B'].profile_list.append(profile)
    profile_2 = Profile()
    profile_2.set_profile('LP_buy', 'child', 'LFLIE', '/', '-', 'add', '0800-OPS1-MDF')
    BOM['B'].profile_list.append(profile_2)

    BOM['B'].apply_profile()
    BOM['B'].update()

    for key in BOM['B'].uid_bom:
        print('Key: {}\n{}'.format(key, BOM['B'].bom[key]))
    '''
    if request.method == 'POST':
        profile_data = request.form['profile_data']
        print(type(profile_data))
        if profile_data['action'] is 'add':
            print('add');
        elif profile_data['action'] is 'remove':
            print('remove')
    profiles = mProfile.query.all()
    bom_index = ['A', 'B']
    return render_template('profile_processing.html', profiles=profiles, bom_index=bom_index)