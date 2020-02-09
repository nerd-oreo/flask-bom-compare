from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SelectSheetForm(FlaskForm):
    select_sheet_a = SelectField('Select worksheet contain BOM A', validators=[DataRequired()])
    select_sheet_b = SelectField('Select worksheet contain BOM B', validators=[DataRequired()])
    next_step = SubmitField('NEXT STEP')


class MappingHeaderForm(FlaskForm):
    select_col_level_a = SelectField('Level', validators=[DataRequired()])
    select_col_number_a = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_a = SelectField('Description', validators=[DataRequired()])
    select_col_rev_a = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_a = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_a = SelectField('Reference Designator', validators=[DataRequired()])
    select_col_mfg_name_a = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_a = SelectField('Manufacturer Part Number', validators=[DataRequired()])

    select_col_level_b = SelectField('Level', validators=[DataRequired()])
    select_col_number_b = SelectField('Item Number', validators=[DataRequired()])
    select_col_desc_b = SelectField('Description', validators=[DataRequired()])
    select_col_rev_b = SelectField('Revision', validators=[DataRequired()])
    select_col_qty_b = SelectField('Quantity', validators=[DataRequired()])
    select_col_ref_des_b = SelectField('Reference Designator', validators=[DataRequired()])
    select_col_mfg_name_b = SelectField('Manufacturer Name', validators=[DataRequired()])
    select_col_mfg_number_b = SelectField('Manufacturer Part Number', validators=[DataRequired()])
    next_step = SubmitField('NEXT STEP')