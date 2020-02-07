class Helper(object):
    """ To grouping all utilities functions """
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