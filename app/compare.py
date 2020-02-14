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
        i = j = 0
        row = 3
        a_queue = b_queue = list()
        
        print('Bom A: {}'.format(self.__bom_a.uid_bom))

        while True:
            if i < len(self.__bom_a.uid_bom):
                bom_a_uid = self.__bom_a.uid_bom[i]
            if j < len(self.__bom_b.uid_bom):
                bom_b_uid = self.__bom_b.uid_bom[j]
            
            print('Compare {}  :  {}'.format(bom_a_uid, bom_b_uid))
            if bom_a_uid == bom_b_uid:
                if len(a_queue) > 0 or len(b_queue) > 0:
                    print('Has uid in queue')
                    temp_bom_a_uid = bom_a_uid
                    temp_bom_b_uid = bom_b_uid
                    if len(a_queue) > 0:
                        print('Pop a_queue')
                        for k in range(0, len(a_queue)):
                            bom_a_uid = a_queue.pop(0)
                            item_a = self.__bom_a.bom[bom_a_uid]
                            ws = write_to_worksheet(ws, row, column['A'], item_a, column['CHANGE']['NIB'])
                            
                            print(a_queue)
                            
                            row += 1
                    if len(b_queue) > 0:
                        print('Pop p_queue')
                        for l in range(0, len(b_queue)):
                            bom_b_uid = b_queue.pop(0)
                            item_b = self.__bom_b.bom[bom_b_uid]
                            ws = write_to_worksheet(ws, row, column['B'], item_b, column['CHANGE']['NIA'])
                            
                            print(b_queue)
                            
                            row += 1
                    bom_a_uid = temp_bom_a_uid
                    bom_b_uid = temp_bom_b_uid
                    
                item_a = self.__bom_a.bom[bom_a_uid]
                ws = write_to_worksheet_ref(ws, row, column['A'], item_a, column['CHANGE'], column['REF_DES_CHANGE']['A'])
                
                item_b = self.__bom_b.bom[bom_b_uid]
                ws = write_to_worksheet_ref(ws, row, column['B'], item_b, column['CHANGE'], column['REF_DES_CHANGE']['B'])
                i += 1; j += 1
                row += 1
                print('Matched\n')
                    
            elif bom_a_uid != bom_b_uid:
                print('Not matched')
                if bom_a_uid in self.__uid_in_a and bom_b_uid in self.__uid_in_b:
                    print('Add both uid to queue')
                    
                    a_queue.append(bom_a_uid)
                    b_queue.append(bom_b_uid)
                    i += 1; j += 1
                    
                    print('a_queue : {}'.format(a_queue))
                    print('\n')
                    print('b_queue : {}'.format(b_queue))
                elif bom_a_uid in self.__uid_in_both and bom_b_uid in self.__uid_in_b:
                    b_queue.append(bom_b_uid)
                    j += 1                    
                    print('Add {} to queue'.format(bom_b_uid))
                    print('b_queue : {}'.format(b_queue))
                elif bom_b_uid in self.__uid_in_both and bom_a_uid in self.__uid_in_a:
                    a_queue.append(bom_a_uid)
                    i += 1
                    print('Add {} to queue'.format(bom_a_uid))
                    print('b_queue : {}'.format(a_queue))

            if i > len(self.__bom_a.uid_bom) and j < len(self.__bom_b.uid_bom):
                for k in range(j, len(self.__bom_b.uid_bom)):
                    bom_b_uid = self.__bom_b.uid_bom[k]
                    item_b = self.__bom_b.bom[bom_b_uid]
                    ws = write_to_worksheet(ws, row, column['B'], item_b, column['CHANGE']['NIA'])
                    row += 1; j += 1
            
            if i < len(self.__bom_a.uid_bom) and j > len(self.__bom_b.uid_bom):
                for k in range(i, len(self.__bom_a.uid_bom)):
                    bom_a_uid = self.__bom_a.uid_bom[k]
                    item_a = self.__bom_a.bom[bom_a_uid]
                    ws = write_to_worksheet(ws, row, column['A'], item_a, column['CHANGE']['NIB'])
                    row += 1; i += 1
            
            if i >= len(self.__bom_a.uid_bom) and j >= len(self.__bom_b.uid_bom):
                break
        wb.save(self.result_path)

    def __template_init(self):
        print('Running __template_init()')
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
        print('Running __compare_uid_bom()')
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
        print('Running __compare_item()')
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
