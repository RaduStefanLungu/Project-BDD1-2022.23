import Attribute,Relation

class Expression(object):

    def __init__(self,attribute_list,relation_list):
        # if attribute_list === ["all"] <=> *  example : Select * from relation_list

        self.is_root:bool = False    # root of the tree (if is root, on execute, it will auto-execute the children if their type is Expression)
        self.attributes = attribute_list
        self.relations = relation_list
        self.QUERY_TYPE:str = "Expression"   # example : Select/Project/Join etc.

        self.sql_query = ""
        pass
    
    def set_is_root(self,value:bool):
        self.is_root = value
    
    def get_is_root(self):
        return self.is_root

    def execute(self):
        # transforms the expression as SQL querry and saves it inside self.sql_query
        pass

    def __str__(self):
        # Prints the Expression as example: 
        # Select('R','S') from Table
        return f"{self.QUERY_TYPE} {self.attributes} FROM {self.relations}"




test = Expression(["A1"],["R"])
print(test)
test.execute()
