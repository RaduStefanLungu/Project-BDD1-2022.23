
class Relation(object):
    # Basically the name (with every data) of a Table (Relation)

    def __init__(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__ (self):
        return self.name

