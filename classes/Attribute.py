
"""
    Class used to define Data Base attribute(column in a table).
    To get this relation name for usage(e.g. in a SQL query) use str(your_attribute)
        but also get_name() method exists.
"""
class Attribute(object):

    def __init__(self,name:str,data_type:str,data_list):
        self.name = name
        self.data_type = data_type.upper()
        self.data_list = data_list

    def get_name(self):
        return self.name

    def get_data_type(self):
        return self.data_type

    def get_data(self):
        return self.data_list

    def get_info(self):
        return "Attribute: '"+self.name+"'" + "_____" + self.data_type

    def print_meta(self):
        print(f"Attribute({self.name}) of type {self.data_type}")
        
    def print_full_meta(self):
        print(f"Attribute({self.name}) of type {self.data_type} contains {self.data_list}")

    def __str__(self):
        return self.name

