class Item:
    def __init__(self):
        # unique id of each item, format:
        # <parent_level>:<parent_number>:<child_level>:<child_number>
        self.unique_id = ''
        self.type = ''
        self.level = 0
        self.number = ''
        self.description = ''
        self.rev = ''
        self.quantity = 0
        self.ref_des = list()
        self.avl = list()  # avl list as list of dict
        self.parent = None
        self.change_status = list()

    def __repr__(self):
        s = 'Unique Id: {}\n' \
            'Type: {}\n' \
            'Parent: {}\n' \
            'Level: {}\n' \
            'Number: {}\n' \
            'Description: {}\n' \
            'Rev: {}\n' \
            'Qty: {}\n' \
            'Ref_Des: {}\n' \
            'AVL: {}\n'.format(self.unique_id, self.type, self.parent.number, self.level, self.number, self.description, self.rev,
                               self.quantity, self.ref_des, self.avl)
        return s

    def set_item(self, level, number, description, rev, quantity):
        self.level = level
        self.number = number
        self.description = description.encode('utf-8')
        self.rev = rev
        self.quantity = quantity

    def _set_unique_id(self):
        if self.parent is None:
            self.unique_id = '{}:{}'.format(self.level, self.number)
        else:
            self.unique_id = '{}:{}:{}:{}'.format(self.parent.level, self.parent.number, self.level, self.number)

    def set_ref_des(self, ref_des, delimiter):
        if ref_des is not None:
            self.ref_des = ref_des.split(delimiter)

    def set_avl(self, mfg_name, mfg_number):
        temp = {mfg_name: mfg_number}
        self.avl.append(temp)

    def set_parent(self, parent=None):
        self.parent = parent
        self._set_unique_id()

    def update_unique_id(self):
        if self.parent is None:
            self.unique_id = '{}:{}'.format(self.level, self.number)
        else:
            self.unique_id = '{}:{}:{}:{}'.format(self.parent.level, self.parent.number, self.level, self.number)