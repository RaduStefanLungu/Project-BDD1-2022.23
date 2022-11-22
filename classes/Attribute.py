
class Attribute(object):
    # Basically just the Name of each Column in a Relation(Table)

    def __init__(self,name,*args):
        self.name = name
        pass


    def __str__(self):
        return self.name



#defining something something