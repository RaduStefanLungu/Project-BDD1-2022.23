import Expression

class Project(Expression):
    def __init__(self,attribute_list,relation):
        self.attribute_list = attribute_list
        self.relation = relation

        
