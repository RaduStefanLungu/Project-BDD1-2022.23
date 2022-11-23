'''
    Probleme rencontre :
        1. Vu que on doit pouvoir embriquer toutes les expressions , j'ai du verifier cela pour mieux formatter le string de sortie
            grace aux methodes utilitaires (transform_list_to_goodString,type_attribute_to_string_inside_expression)
            sachant que pour rajouter tt les classes dans Expression.class_type_list[] , je devrais import tt les classes dans le fichier de l'object Expression
            Vu que j'avais du aussi import le fichier Expression.py dans le fichier avec tt les requetes(Requests.py) il y a vait un 
            cycle d'import. Pour eviter cela , malgre que dans la programmation oriente objet on doit faire principalement un fichier par objet,
            j'ai du tout concatener dans un seul fichier pour eviter le cycle d'import 
'''

class Expression(object):
    
    def __init__(self,attribute_list,relation_list,SPJRUD_type:str,QUERY_TYPE:str):

        # if attribute_list === ["all"] <=> *  example : Select * from relation_list

        self.attributes = attribute_list
        self.relations = relation_list
        self.SPJRUD_type:str = SPJRUD_type
        self.QUERY_TYPE:str = QUERY_TYPE   # example : Select/Project/Join etc.
        self.other_query_addons = ""    # ment to be changed manually due to function order calls.
        self.sql_query = ""     # ment to be send to SQLite DB
        self.class_type_list = [Expression,Select,Project,Rename,Join,Difference,Union] # list of children class types * MUST BE UPDATED FOR EVERY NEW CHILDREN IN THE CODE ! *
    
    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self):
        # transforms the expression as SQL querry and saves it inside self.sql_query
        
        # TODO Before it saves itself to self.sql_query , DO THE CHECKING(from the db) + Error manager!!

        for attribute in self.attributes:
            if type(attribute) == Expression:
                attribute.execute()

        self.sql_query = self.proper_str(self.class_type_list,self.QUERY_TYPE).replace("'","").replace("\\","")

        return self.sql_query

    def get_sql_query(self):
        return self.sql_query

    '''
        This method is used to create the string representation of this class.
        It uses a class_type_list since we're checking nested data within
        @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):
        # Prints the Expression as example: 
        # Select ['A0','A1'] from ["Relation"]

        attList = []
        relList = []

        for a in self.attributes:
            attList.append(type_attribute_to_string_inside_expression(a,class_type_l))
        for r in self.relations:
            relList.append(type_attribute_to_string_inside_expression(r,class_type_l))

        attString = transform_list_to_goodString(attList)
        relString = transform_list_to_goodString(relList)

        return f'{wanted_expression} {attString} FROM {relString} {self.other_query_addons}'


    def __str__(self):
        return self.proper_str(self.class_type_list,self.SPJRUD_type)
        

# Tool Method
def transform_list_to_goodString(myList):
    t = str(tuple(myList))
    if len(myList)== 1 :
            t = t[:len(t)-2]+")"

    t = str(myList)
    t = t.replace("\"", "")
    t = t.replace("]","").replace("[","")
    return t


# Tool Method
# method that writes in sql format the given attribute
def type_attribute_to_string_inside_expression(myAttribute,class_type_list):

    if type(myAttribute) in class_type_list :
        return "( "+str(myAttribute)+" )"
    else:
        return str(myAttribute)


class Select(Expression):
    # def __init__(self):
    #     Expression.__init__(self, ExpressionType.Select)

    def __init__(self,attributes_list,wanted_values_list,operation:str,relation):
        if len(attributes_list) != len(wanted_values_list):
            raise ValueError("Invalid number of attributes/wanted_values")
        # other_query_addons = self.create_query_addon(attributes_list,wanted_values_list,operation)
        
        super().__init__(attributes_list,[relation],"Select","Select")

        self.other_query_addons = self.create_query_addon(attributes_list,wanted_values_list,operation)

        self.accepted_operations = ["=",">","<"]
        self.wanted_values_list = wanted_values_list
        self.operation = ""
        if operation.strip() not in self.accepted_operations:
            raise ValueError("Invalid operation \n accepted operations : {self.accepted_operations}")
        else:
            self.operation = operation.strip()

    '''
        Method used to create left part of a SQL query
        @return: in this exact case , it will return 'WHERE Attribute = "Value" '

    '''
    def create_query_addon(self,att_list,wanted_values,operation:str):
        query_addon = "WHERE "
        left_constructor = []
        types_list = self.class_type_list
        x = 0
        while x < len(att_list):
            if type(att_list[x]) in types_list:
                if type(wanted_values[x])== str:
                    temp = "("+str(att_list[x])+")" + operation + '"'+wanted_values[x]+'"'
                else:
                    temp = "("+str(att_list[x])+")" + operation + str(wanted_values[x])
            else : 
                if type(wanted_values[x])== str:
                    temp = str(att_list[x]) + operation + '"'+wanted_values[x]+'"'
                else:
                    temp = str(att_list[x]) + operation + str(wanted_values[x])
            
            
            left_constructor.append(temp)
            x += 1

        query_addon += ','.join(left_constructor)

        return query_addon


class Project(Expression):
    def __init__(self,attribute_list,relation):
        super().__init__(attribute_list,[relation],"Project","Select")


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
        

