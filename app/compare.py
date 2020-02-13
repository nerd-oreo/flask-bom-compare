from openpyxl import Workbook
from app.item import Item

class Compare:
    def __init__(self, bom_a, bom_b):
        self.__bom_a = bom_a
        self.__bom_b = bom_b
        self.__uid_in_a = list()
        self.__uid_in_b = list()
        self.__uid_in_both = list()
        
    def compare(self):
        self.__compare_uid_bom()
        self.__compare_item()
        
    def generate_report(self):
        wb = Workbook(write_only=True)
        pass
    
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
            