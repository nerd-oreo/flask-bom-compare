from openpyxl import load_workbook
from config import BASE_DIR
from datetime import datetime
from app.utils import write_to_worksheet, write_to_worksheet_ref, get_value, get_max, write_to_worksheet_avl
import shutil
import os


class Compare:
    def __init__(self, bom_a, bom_b):
        self.__bom_a = bom_a
        self.__bom_b = bom_b
        self.__master_list = list()
        self.result_filename = ''
        self.result_file = ''

        if self.__bom_a.has_avl and self.__bom_b.has_avl:
            self.compare_avl = True
        else:
            self.compare_avl = False

    def compare(self):
        column = {
            'A': {'level': 'A', 'number': 'B', 'description': 'C', 'rev': 'D', 'qty': 'E', 'ref_des': 'F'},
            'B': {'level': 'G', 'number': 'H', 'description': 'I', 'rev': 'J', 'qty': 'K', 'ref_des': 'L'},
            'CHANGE': {'NIA': 'M', 'NIB': 'N', 'description': 'O', 'rev': 'P', 'qty': 'Q', 'ref_des': 'R'},
            'REF_DES_CHANGE': {'A': 'S', 'B': 'T'},
        }
        row = 3     # start row
        self.__template_init()

        # Prepare working for writing report
        wb = load_workbook(self.result_file)
        ws = wb['GENERIC COMPARE']

        if self.compare_avl:
            avl_ws = wb['AVL COMPARE']
            avl_row = 3
            avl_column = {
                'A': {'number': 'A', 'mfg_name': 'B', 'mfg_number': 'C'},
                'B': {'number': 'D', 'mfg_name': 'E', 'mfg_number': 'F'},
            }

        # create UID master list
        for i in range(get_max(self.__bom_a.uid, self.__bom_b.uid)):
            uid_a = get_value(i, self.__bom_a.uid)
            uid_b = get_value(i, self.__bom_b.uid)
            if uid_a == uid_b:
                self.__master_list.append(uid_a)
            else:
                if uid_a not in self.__master_list and uid_a is not None:
                    self.__master_list.append(uid_a)
                elif uid_b not in self.__master_list and uid_b is not None:
                    self.__master_list.append(uid_b)

        # start comparing
        for i in range(len(self.__master_list)):
            uid = self.__master_list[i]
            # if uid exist in both bom A and bom B
            if uid in self.__bom_a.uid and uid in self.__bom_b.uid:
                # comparing item detail
                self.__compare_item(uid)
                item_a = self.__bom_a.bom[uid]
                item_b = self.__bom_b.bom[uid]
                ws = write_to_worksheet_ref(ws, row, column['A'], item_a, column['CHANGE'],
                                            column['REF_DES_CHANGE']['A'])
                ws = write_to_worksheet_ref(ws, row, column['B'], item_b, column['CHANGE'],
                                            column['REF_DES_CHANGE']['B'])

                # Compare AVL
                if self.compare_avl:
                    if len(item_a.avl_uid) is not 0 or len(item_b.avl_uid) is not 0:
                        avl_master_list = list()
                        # create AVL UID master list
                        for j in range(get_max(item_a.avl_uid, item_b.avl_uid)):
                            avl_uid_a = get_value(j, item_a.avl_uid)
                            avl_uid_b = get_value(j, item_b.avl_uid)
                            if avl_uid_a == avl_uid_b:
                                avl_master_list.append(avl_uid_a)   # only append one uid if both are matched
                            else:
                                if avl_uid_a not in avl_master_list and avl_uid_a is not None:
                                    avl_master_list.append(avl_uid_a)
                                elif avl_uid_b not in avl_master_list and avl_uid_b is not None:
                                    avl_master_list.append(avl_uid_b)
                        # start compare AVL
                        for j in range(len(avl_master_list)):
                            avl_uid = avl_master_list[j]
                            if avl_uid in item_a.avl_uid and avl_uid in item_b.avl_uid:
                                for mfg_name, mfg_number in item_a.avl[avl_uid].items():
                                    avl_ws = write_to_worksheet_avl(avl_ws, avl_row, avl_column['A'], item_a.number, mfg_name, mfg_number)
                                for mfg_name, mfg_number in item_b.avl[avl_uid].items():
                                    avl_ws = write_to_worksheet_avl(avl_ws, avl_row,  avl_column['B'], item_b.number, mfg_name, mfg_number)
                            else:
                                if avl_uid in item_a.avl_uid:
                                    for mfg_name, mfg_number in item_a.avl[avl_uid].items():
                                        avl_ws = write_to_worksheet_avl(avl_ws, avl_row,  avl_column['A'], item_a.number,
                                                                        mfg_name, mfg_number)
                                elif avl_uid in item_b.avl_uid:
                                    for mfg_name, mfg_number in item_b.avl[avl_uid].items():
                                        avl_ws = write_to_worksheet_avl(avl_ws, avl_row,  avl_column['B'], item_b.number,
                                                                        mfg_name, mfg_number)
                            avl_row += 1
            else:
                if uid in self.__bom_a.uid:
                    item_a = self.__bom_a.bom[uid]
                    ws = write_to_worksheet(ws, row, column['A'], item_a, column['CHANGE']['NIB'])
                elif uid in self.__bom_b.uid:
                    item_b = self.__bom_b.bom[uid]
                    ws = write_to_worksheet(ws, row, column['B'], item_b, column['CHANGE']['NIA'])
            row += 1
        wb.save(self.result_file)

    def __template_init(self):
        print('Running __template_init()')
        src_folder = BASE_DIR + '\\app\\static\\xlsx\\'
        src_file = os.path.join(src_folder, 'result.xlsx')

        dst_folder = BASE_DIR + '\\app\\download\\'
        dst_filename = 'result_' + datetime.now().strftime('%Y%m%d%H%M%S%f') + '_.xlsx'
        dst_file = os.path.join(dst_folder, dst_filename)
        shutil.copy2(src_file, dst_file)
        print('Generate report at {}'.format(dst_file))
        self.result_filename = dst_filename
        self.result_file = dst_file

    def __compare_item(self, uid):
        item_a = self.__bom_a.bom[uid]
        item_b = self.__bom_b.bom[uid]

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
