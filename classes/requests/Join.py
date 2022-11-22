import Expression

class Join(Expression):
    def __init__(self, relations_list):
        self.relations_list = relations_list