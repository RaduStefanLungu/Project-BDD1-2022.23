
"""
    Class used to define a Data Base relation(table).
    To get this relation name for usage(e.g. in a SQL query) use str(your_relation)
        but also get_name() method exists.
    To print data about your object, use print_meta() method .
"""
class Relation(object):

    def __init__(self,name:str,attributes_list):
        self.name = name
        self.attributes_list = attributes_list
    
    def get_name(self):
        return self.name
    
    def get_attributes_list(self):
        return self.attributes_list

    def print_meta(self):
        print(f"Relation({self.name}) contains : {str(self.attributes_list)}")

    def __str__ (self):
        return self.name

