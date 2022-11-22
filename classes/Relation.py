
class Relation(object):
    # Basically the name (with every data) of a Table (Relation)

    def __init__(self,name,*args):
        self.name = name
        pass

    def __str__ (self):
        return self.name

