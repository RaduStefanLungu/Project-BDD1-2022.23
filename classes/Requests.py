from Expression import Expression


class Select(Expression):
    
    def __init__(self,attributes_list,wanted_values_list,operation:str,relation):
        super(attributes_list,[relation])
        self.accepted_operations = ["=",">","<"]
        self.wanted_values_list = wanted_values_list
        self.operation = ""
        if operation.strip() not in self.accepted_operations:
            raise ValueError("Invalid operation \n accepted operations : {self.accepted_operations}")
        else:
            self.operation = operation.strip()

        self.QUERY_TYPE = "Select"

class Project(Expression):
    def __init__(self,attribute_list,relation):
        self.attribute_list = attribute_list
        self.relation = relation


class Rename(Expression):
    def __init__(self, attribute_list, new_names_list):
        self.attribute_list = attribute_list
        self.new_names_list = new_names_list


class Join(Expression):
    def __init__(self, relations_list):
        self.relations_list = relations_list


class Difference(Expression):
    def __init__(self, r1,r2):
        self.r1 = r1
        self.r2 = r2


class Union(Expression):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        


x = Select(["A","B"],["Charleroi","Bruge"],"=","R")

print(x+"\n")
x.execute()
print("--> executed x :"+x + "\n")