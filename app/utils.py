from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ALLOWED_EXTENSIONS = {'xlsx'}


def map_header_to_letter(filename, sheet_name):
    header_list = list()
    header_list.append(('', ''))
    wb = load_workbook(filename=filename, read_only=False)

    ws = wb[sheet_name]
    for i in range(1, ws.max_column):
        c = ws.cell(row=1, column=i)
        col_n = get_column_letter(i)
        header_list.append((col_n,c.value))
    return header_list


def get_worksheet_choices(filename):
    wb = load_workbook(filename=filename, read_only=False)
    ws_choices = list()
    ws_choices.append(('', ''))
    for s in wb.sheetnames:
        ws_choices.append((s, s))
    return ws_choices


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_qty_to_number(qty):
    if qty == "None":
        return None
    else:
        try:
            return int(qty)
        except ValueError:
            return float(qty)


def convert_level_to_number(level):
    try:
        return int(level)
    except (TypeError, ValueError):
        return None