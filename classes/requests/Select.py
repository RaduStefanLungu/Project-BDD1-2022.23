import Expression

class Select(Expression):
    
    def __init__(self,att_list,wanted_values_list,operation:str,relation):
        self.att_list = att_list
        self.wanted_values_list = wanted_values_list
        self.operation = operation
        self.relation = relation

