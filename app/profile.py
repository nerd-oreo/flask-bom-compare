class Profile:
    def __init__(self):
        self.profile_name = ''
        self.item_type = ''
        self.customer = ''
        self.prefix = ''
        self.prefix_action = ''     # add, remove, ignore, not apply
        self.suffix = ''
        self.suffix_action = ''     # add, remove, not apply
        self.delimiter = ''
        self.delimiter_action = ''  # add, remove, not apply
        self.delimiter_sample = ''

    def set_profile(self, profile_name, item_type, customer, prefix, prefix_action, suffix, suffix_action, delimiter, delimiter_action, delimiter_sample):
        self.profile_name = profile_name
        self.item_type = item_type
        self.customer = customer
        self.prefix = prefix
        self.prefix_action = prefix_action
        self.suffix = suffix
        self.suffix_action = suffix_action
        self.delimiter = delimiter
        self.delimiter_action = delimiter_action
        self.delimiter_sample = delimiter_sample

    def apply(self, number):
        delimiter_pos = list()

        # remove prefix
        if self.prefix_action == 'add':
            if self.prefix not in number:
                number = self.prefix + number
        elif self.prefix_action == 'remove':
            if self.prefix in number:
                number = number.replace(self.prefix, '')
        elif self.prefix_action == 'ignore':
            pass

        # remove suffix
        if self.suffix_action == 'add':
            number = number + self.suffix
        elif self.suffix_action == 'remove':
            number = number.split(self.suffix)[0]

        if self.delimiter_action == 'add':
            if self.delimiter not in number:
                for i in range(0, len(self.delimiter_sample)):
                    c = self.delimiter_sample[i]
                    if c == self.delimiter:
                        delimiter_pos.append(i)

                for i in range(0, len(delimiter_pos)):
                    pos = delimiter_pos[i]
                    number = number[:pos] + self.delimiter + number[pos:]
        elif self.delimiter_action == 'remove':
            number = number.replace(self.delimiter, '')

        return number
