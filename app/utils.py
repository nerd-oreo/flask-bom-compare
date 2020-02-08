from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ALLOWED_EXTENSIONS = {'xlsx'}


def map_header_to_letter(filename):
    header_list = list()
    wb = load_workbook(filename=filename, read_only=False)

    ws = wb.worksheets[0]
    for i in range(1, ws.max_column):
        c = ws.cell(row=1, column=i)
        col_n = get_column_letter(i)
        header_list.append({c.value : col_n})
    return header_list


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
