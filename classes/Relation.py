
class Relation(object):
    # Relation (table) that can be empty or contain multiple attributes with data
    # 
    # TODO : Add an attributeList to this  

    def __init__(self,name:str):
        self.name = name

    def get_name(self):
        return self.name

    def print_meta(self):
        print(f"Relation({self.name})")

    def __str__ (self):
        return self.name

