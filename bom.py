from openpyxl import load_workbook
from item import Item
from helper import Helper

class BomCompare:
    def __init__(self):
        self.BOM_A = dict()     # {unique_id:item}
        self.uid_BOM_A = list() # unique id list for BOM A
        self.BOM_B = dict()
        self.uid_BOM_B = list() # unique id list for BOM A
        
    def load_xls(self, filename=None, columns=None):
        def load(ws):
            BOM = dict()
            uid_BOM = list()
            parent_stack = list()
            current_parent = None
            last_item = None

            for row in range(2, ws.max_row+1):
                level = ws[col_level + str(row)].value
                
                if level != None:
                    # get data from excel sheet
                    level = Helper.convert_level_to_number(str(ws[col_level + str(row)].value))
                    number = str(ws[col_number + str(row)].value)
                    description = str(ws[col_description + str(row)].value)
                    rev = str(ws[col_rev + str(row)].value).split(" ")[0]
                    qty = Helper.convert_qty_to_number(str(ws[col_qty + str(row)].value))
                    
                    item = Item()
                    item.set_item(level, number, description, rev, qty)
                    
                    if ws[col_ref_des + str(row)].value != None:
                        ref_des = str(ws[col_ref_des + str(row)].value)
                        item.set_ref_des(ref_des)
                        
                    if ws[col_mfg_name + str(row)].value != None and ws[col_mfg_number + str(row)].value != None:
                        mfg_name = str(ws[col_mfg_name + str(row)].value)
                        mfg_number = str(ws[col_mfg_number + str(row)].value)
                        item.set_avl(mfg_name, mfg_number)
                    
                    if item.level == 0:                 # top level
                        current_parent = item
                        item.set_parent()
                    elif item.level > last_item.level:  # swapping to a lower level
                        parent_stack.append(current_parent)
                        current_parent = last_item   
                    elif item.level < last_item.level:  # swapping back to upper level
                        current_parent = parent_stack.pop()
                    elif item.level == last_item.level:
                        pass
                    item.set_parent(parent=current_parent)
                    BOM[item.unique_id] = item
                    uid_BOM.append(item.unique_id)
                    last_item = item

                else: # if level is None type, only collect data from column V and X
                    mfg_name = str(ws[col_mfg_name + str(row)].value)
                    mfg_number = str(ws[col_mfg_number + str(row)].value)
                    
                    key = uid_BOM[len(uid_BOM)-1]
                    item = BOM[key]
                    item.set_avl(mfg_name,mfg_number)
                    BOM.update({key:item})

            return BOM, uid_BOM
        
        if len(columns) != 8:
            raise Exception('Number of columns isn\'t matched.')
        else:
            col_level, col_number, col_description, col_qty, col_rev, col_ref_des, col_mfg_name, col_mfg_number = columns

            wb = load_workbook(filename=filename,read_only=False)
            if len(wb.sheetnames) != 2:
                raise Exception('Less or more than two sheets in the template.')
            else:
                self.BOM_A, self.uid_BOM_A = load(wb.worksheets[0])
                #self.BOM_B, self.uid_BOM_B = load(wb.worksheets[1])

