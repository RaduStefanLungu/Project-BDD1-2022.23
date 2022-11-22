
class Attribute(object):
    # Basically just the Name of each Column in a Relation(Table)

    def __init__(self,name):
        self.name = name

    def get_name(self):
        return self.name



    def __str__(self):
        return self.name

