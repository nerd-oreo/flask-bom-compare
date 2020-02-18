from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired

from app.models import Profile


class SelectSheetForm(FlaskForm):
    select_sheet_a = SelectField('Worksheet in BOM A', validators=[DataRequired()])
    select_sheet_b = SelectField('Worksheet in BOM B', validators=[DataRequired()])
    next_step = SubmitField('NEXT STEP')


class MappingHeaderForm(FlaskForm):
    select_col_level_a = SelectField('Level', validators=[DataRequired()])
    select_col_number_a = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_a = SelectField('Description', validators=[DataRequired()])
    select_col_rev_a = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_a = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_a = SelectField('Ref Des', validators=[DataRequired()])
    select_col_ref_des_delimiter_a = SelectField('Ref Des  Delimiter', validators=[DataRequired()])
    select_col_mfg_name_a = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_a = SelectField('Manufacturer Part Number', validators=[DataRequired()])

    select_col_level_b = SelectField('Level', validators=[DataRequired()])
    select_col_number_b = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_b = SelectField('Description', validators=[DataRequired()])
    select_col_rev_b = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_b = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_b = SelectField('Ref Des', validators=[DataRequired()])
    select_col_ref_des_delimiter_b = SelectField('Ref Des Delimiter', validators=[DataRequired()])
    select_col_mfg_name_b = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_b = SelectField('Manufacturer Part Number', validators=[DataRequired()])
    next_step = SubmitField('NEXT STEP')


class MappingHeaderUsingTemplateForm(FlaskForm):
    template_radio = RadioField('Templates', coerce=int, validators=[InputRequired()])
    use_template = SubmitField('USE TEMPLATE')


class NewMappingTemplateForm(FlaskForm):
    template_name = StringField('Template Name', validators=[DataRequired()])
    customer = StringField('Customer')
    select_col_level_a = SelectField('Level', validators=[DataRequired()])
    select_col_number_a = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_a = SelectField('Description', validators=[DataRequired()])
    select_col_rev_a = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_a = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_a = SelectField('Ref Des', validators=[DataRequired()])
    select_col_ref_des_delimiter_a = SelectField('Ref Des  Delimiter', validators=[DataRequired()])
    select_col_mfg_name_a = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_a = SelectField('Manufacturer Part Number', validators=[DataRequired()])

    select_col_level_b = SelectField('Level', validators=[DataRequired()])
    select_col_number_b = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_b = SelectField('Description', validators=[DataRequired()])
    select_col_rev_b = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_b = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_b = SelectField('Ref Des', validators=[DataRequired()])
    select_col_ref_des_delimiter_b = SelectField('Ref Des Delimiter', validators=[DataRequired()])
    select_col_mfg_name_b = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_b = SelectField('Manufacturer Part Number', validators=[DataRequired()])
    next_step = SubmitField('ADD TEMPLATE')


class NewProfileForm(FlaskForm):
    profile_name = StringField('Profile Name', validators=[DataRequired()])
    item_type = SelectField('Item Type', choices=[('parent', 'parent'), ('child', 'child')], validators=[DataRequired()])
    customer = StringField('Customer')
    prefix = StringField('Prefix')
    prefix_action = SelectField('Prefix Action', choices=[('not apply', 'not apply'), ('add', 'add'), ('remove', 'remove'), ('ignore', 'ignore')], validators=[DataRequired()])
    suffix = StringField('Suffix')
    suffix_action = SelectField('Suffix Action', choices=[('not apply', 'not apply'), ('add', 'add'), ('remove', 'remove')], validators=[DataRequired()])
    delimiter = StringField('Delimiter')
    delimiter_action = SelectField('Delimiter Action', choices=[('not apply', 'not apply'), ('add', 'add'), ('remove', 'remove')], validators=[DataRequired()])
    delimiter_sample = StringField('Delimiter Sample')
    add_profile = SubmitField('Add Profile')
