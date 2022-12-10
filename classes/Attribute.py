
"""
    Class used to define Data Base attribute(column in a table).
    To get this relation name for usage(e.g. in a SQL query) use str(your_attribute)
        but also get_name() method exists.
"""
class Attribute(object):
    possible_data_type = ["INT","REAL","TEXT","CHAR"]

    def __init__(self,name:str,data_type:str,primary_key:bool,not_null:bool,data_list):
        self.primary_key = primary_key
        self.not_null = not_null
        self.name = name
        self.data_type = ""
        if (data_type.upper().strip() in self.possible_data_type) or (data_type.upper().strip()[:4] in self.possible_data_type):
            self.data_type = data_type.upper()
        else:
            if self.name != "*":
                #TODO
                raise ValueError("\nN/A CALL CUSTOM ERRORS\n")
                

        self.data_list = data_list

    def get_name(self):
        return self.name

    def get_data_type(self):
        return self.data_type

    def get_data(self):
        return self.data_list

    def get_info(self):
        return f"Attribute: '{self.name}'_____{self.data_type}_____NOT NULL:{self.not_null}"

    def print_meta(self):
        print(f"Attribute({self.name}) of type {self.data_type}")
        
    def print_full_meta(self):
        print(f"Attribute({self.name}) of type {self.data_type} contains {self.data_list}")

    def __str__(self):
        return self.name

