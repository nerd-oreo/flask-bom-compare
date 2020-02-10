class Profile:
    def __init__(self):
        self.profile_name = ''
        self.type = ''
        self.prefix = ''
        self.suffix = ''
        self.delimiter = ''
        self.action = ''
        self.sample = ''

    def set_profile(self, profile_name, type, prefix, suffix, delimiter, action, sample):
        self.profile_name = profile_name
        self.type = type
        self.prefix = prefix
        self.suffix = suffix
        self.delimiter = delimiter
        self.action = action
        self.sample = sample

    def apply(self, number):
        delimiter_pos = list()

        # remove prefix
        if self.prefix in number:
            number = number.replace(self.prefix, '')
            # remove suffix
            if self.suffix in number:
                number = number.split(self.suffix)[0]

            if self.delimiter not in number:
                for i in range(0, len(self.sample)):
                    c = self.sample[i]
                    if c == self.delimiter:
                        delimiter_pos.append(i)

                if self.action is 'add':
                    for i in range(0, len(delimiter_pos)):
                        pos = delimiter_pos[i]
                        number = number[:pos] + self.delimiter + number[pos:]
                elif self.action is 'remove':
                    number = number.replace(self.delimiter, '')
                else:
                    pass

        return number
