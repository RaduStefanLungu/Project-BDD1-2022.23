
class Attribute(object):
    # Attribute(column) of a Relation(Table).
    # It contains data

    # TODO Add dataList and dataType to this ! 

    def __init__(self,name:str,data_type:str):
        self.name = name
        self.data_type = data_type.upper()

    def get_name(self):
        return self.name

    def get_data_type(self):
        return self.data_type

    def get_info(self):
        return "'"+self.name+"'" + "_____" + self.data_type

    def __str__(self):
        return self.name

