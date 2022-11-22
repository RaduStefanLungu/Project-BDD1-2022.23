from classes.Attribute import Attribute
from classes.Relation import Relation

class Expression(object):

    def __init__(self,attribute_list,relation_list):
        # if attribute_list === ["all"] <=> *  example : Select * from relation_list

        self.attributes = attribute_list
        self.relations = relation_list
        self.QUERY_TYPE:str = "Expression"   # example : Select/Project/Join etc.

        self.sql_query = ""     # ment to be send to SQLite DB
        pass
    
    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self):
        # transforms the expression as SQL querry and saves it inside self.sql_query
        
        # TODO Before it saves itself to self.sql_query , DO THE CHECKING(from the db) + Error manager!!

        for attribute in self.attributes:
            if type(attribute) == Expression:
                attribute.execute()

        self.sql_query = str(self)

        return str(self)

    def get_sql_query(self):
        return self.sql_query

    def __str__(self):
        from tools.sql_string_formatter import transform_list_to_goodString,type_attribute_to_string_inside_expression

        # Prints the Expression as example: 
        # Select ['A0','A1'] from ["Relation"]

        attList = []
        relList = []

        for a in self.attributes:
            attList.append(type_attribute_to_string_inside_expression(a))
        for r in self.relations:
            relList.append(type_attribute_to_string_inside_expression(r))

        attString = transform_list_to_goodString(attList)
        relString = transform_list_to_goodString(relList)

        return f'{self.QUERY_TYPE} {attString} FROM {relString}'


