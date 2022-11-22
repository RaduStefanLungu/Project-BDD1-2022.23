import Expression

class Rename(Expression):
    def __init__(self, attribute_list, new_names_list):
        self.attribute_list = attribute_list
        self.new_names_list = new_names_list

