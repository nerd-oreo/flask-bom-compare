from openpyxl import load_workbook
from config import BASE_DIR
from datetime import datetime
from app.utils import write_to_worksheet, write_to_worksheet_ref
import shutil
import os


class Compare:
    def __init__(self, bom_a, bom_b):
        self.__bom_a = bom_a
        self.__bom_b = bom_b
        self.__uid_in_a = list()
        self.__uid_in_b = list()
        self.__uid_in_both = list()
        self.result_file = ''
        self.result_path = ''
        
    def compare(self):
        self.__compare_uid_bom()
        self.__compare_item()
        self.__generate_result()
        
    def __generate_result(self):
        column = {
            'A': {'level': 'A', 'number': 'B', 'description': 'C', 'rev': 'D', 'qty': 'E', 'ref_des': 'F'},
            'B': {'level': 'G', 'number': 'H', 'description': 'I', 'rev': 'J', 'qty': 'K', 'ref_des': 'L'},
            'CHANGE': {'NIA': 'M', 'NIB': 'N', 'description': 'O', 'rev': 'P', 'qty': 'Q', 'ref_des': 'R'},
            'REF_DES_CHANGE': {'A': 'R', 'B': 'S'},
        }
        self.__template_init()
        wb = load_workbook(self.result_path)
        ws = wb['GENERIC COMPARE']
        i = 0
        j = 0
        row = 3
        print("len A: {}".format(len(self.__bom_a.uid_bom)))
        print("uid A : ", self.__bom_a.uid_bom)
        print("len B: {}".format(len(self.__bom_b.uid_bom)))
        print("uid A : ", self.__bom_b.uid_bom)
        while True:
            if i < len(self.__bom_a.uid_bom):
                bom_a_uid = self.__bom_a.uid_bom[i]
            if j < len(self.__bom_b.uid_bom):
                bom_b_uid = self.__bom_b.uid_bom[j]

            if bom_a_uid == bom_b_uid and bom_a_uid in self.__uid_in_both and bom_b_uid in self.__uid_in_both:
                item_a = self.__bom_a.bom[bom_a_uid]
                ws = write_to_worksheet_ref(ws, row, column['A'], item_a, column['CHANGE'], column['REF_DES_CHANGE']['A'])
                item_b = self.__bom_b.bom[bom_b_uid]
                ws = write_to_worksheet_ref(ws, row, column['B'], item_b, column['CHANGE'], column['REF_DES_CHANGE']['B'])

            '''
            if i < len(self.__bom_a.uid_bom):
                bom_a_uid = self.__bom_a.uid_bom[i]
                if bom_a_uid in self.__uid_in_both:
                    item_a = self.__bom_a.bom[bom_a_uid]
                    ws = write_to_worksheet_ref(ws, row, column['A'], item_a, column['CHANGE'], column['REF_DES_CHANGE']['A'])
                elif bom_a_uid in self.__uid_in_a:
                    item_a = self.__bom_a.bom[bom_a_uid]
                    ws = write_to_worksheet(ws, row, column['A'], item_a, column['CHANGE']['NIB'])

            if j < len(self.__bom_b.uid_bom):
                bom_b_uid = self.__bom_b.uid_bom[j]
                if bom_b_uid in self.__uid_in_both:
                    item_b = self.__bom_b.bom[bom_b_uid]
                    ws = write_to_worksheet_ref(ws, row, column['B'], item_b, column['CHANGE'], column['REF_DES_CHANGE']['B'])
                elif bom_b_uid in self.__uid_in_b:
                    row = row + 1
                    item_b = self.__bom_b.bom[bom_b_uid]
                    ws = write_to_worksheet(ws, row, column['B'], item_b, column['CHANGE']['NIA'])
            '''
            if i > len(self.__bom_a.uid_bom) and j > len(self.__bom_b.uid_bom):
                break
            row = row + 1
            i = i + 1
            j = j + 1
        wb.save(self.result_path)

    def __template_init(self):
        src_folder = BASE_DIR + '\\app\\static\\xlsx\\'
        src_file = os.path.join(src_folder, 'result.xlsx')

        dst_folder = BASE_DIR + '\\app\\download\\'
        dst_filename = 'result_' + datetime.now().strftime('%Y%m%d%H%M%S%f') + '_.xlsx'
        dst_file = os.path.join(dst_folder, dst_filename)
        shutil.copy2(src_file, dst_file)
        print('Generate report at {}'.format(dst_file))
        self.result_file = dst_filename
        self.result_path = dst_file

    def __compare_uid_bom(self):
        # compare uid in bom A against uid bom B
        uid_a = self.__bom_a.uid_bom
        uid_b = self.__bom_b.uid_bom
        for i in range(len(uid_a)):
            if uid_a[i] in uid_b:
                self.__uid_in_both.append(uid_a[i])
            else:
                self.__uid_in_a.append(uid_a[i])
        
        for j in range(len(uid_b)):
            if uid_b[j] not in self.__uid_in_both:
                self.__uid_in_b.append(uid_b[j])
                
    def __compare_item(self):
        # compare item which exists in both list
        for i in range(0, len(self.__uid_in_both)):
            id = self.__uid_in_both[i]
            item_a = self.__bom_a.bom[id]
            item_b = self.__bom_b.bom[id]
            
            # compare description
            if item_a.description != item_a.description:
                item_a.change_status.append('c_description')
                item_b.change_status.append('c_description')
            
            # compare rev 
            if item_a.rev != item_b.rev:
                item_a.change_status.append('c_rev')
                item_b.change_status.append('c_rev')
            
            # compare qty
            if item_a.quantity != item_b.quantity:
                item_a.change_status.append('c_qty')
                item_b.change_status.append('c_qty')
            
            # compare ref_des
            for j in range(0, len(item_a.ref_des)):
                a_ref_des = item_a.ref_des[j]
                if a_ref_des not in item_b.ref_des:
                    item_a.ref_des_change.append(a_ref_des)
                    if 'c_ref_des' not in item_a.change_status:
                        item_a.change_status.append('c_ref_des')
                        
            for k in range(0, len(item_b.ref_des)):
                b_ref_des = item_b.ref_des[k]
                if b_ref_des not in item_a.ref_des:
                    item_b.ref_des_change.append(b_ref_des)
                    if 'c_ref_des' not in item_b.change_status:
                        item_b.change_status.append('c_ref_des')
