from classes.Relation import Relation
from classes.Attribute import Attribute
#Colors taken from AINSI CODE from : https://www.geeksforgeeks.org/print-colors-python-terminal/

code_reset = "\033[00m"
code_red = "\033[91m"
code_green = "\033[92m"
code_yellow = "\033[93m"
code_light_purple = "\033[94m"
code_purple = "\033[95m"
code_cyan = "\033[96m"
code_light_gray = "\033[97m"


class Expression(object):
    
    def __init__(self,attribute_list,relation_list,SPJRUD_type:str,QUERY_TYPE:str):

        # if attribute_list === ["all"] <=> *  example : Select * from relation_list

        self.attributes = attribute_list
        self.relations = relation_list
        self.SPJRUD_type:str = SPJRUD_type
        self.QUERY_TYPE:str = QUERY_TYPE    # example : Select/Project/Join etc.
        self.other_query_addons = ""        # ment to be changed manually due to function order calls.
        self.sql_query = "- ! You forgot to use execute() method ! -"     # ment to be send to SQLite DB after usage of execute()
        self.class_type_list = [Expression,Select,Project,Rename,Join,Difference,Union] # list of children class types * MUST BE UPDATED FOR EVERY NEW CHILDREN IN THE CODE ! *
    
    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self,data_base):
        # transforms the expression as SQL querry and saves it inside self.sql_query
        
        # TODO Before it saves itself to self.sql_query , DO THE CHECKING(from the db) + Error manager!!
        self.check_data(data_base)

        for attribute in self.attributes:
            if type(attribute) in self.class_type_list:
                attribute.execute()
        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute()

        self.sql_query = self.proper_str(self.class_type_list,self.QUERY_TYPE).replace("'","").replace("\\","")

        return self.sql_query

    '''
        This method verifies if entered data as SPJRUD query is correct and if it checks within the database.
    '''
    def check_data(self,data_base):
        
        self.check_data_relations(data_base)
        self.check_data_attributes()
        

    """
        Method called inside check_data(...).
        Used to check if the given relations of a query exists within the data base.
        @return True if everything is ok, raises ValueError if not.
    """
    def check_data_relations(self,data_base):
        #checking the relations
        for r in self.relations:
            if r.get_name() not in data_base.relations_list_name:
                raise ValueError(f"""
                The (sub-)expression:
                | {str(self)} | is {code_red}invalid{code_reset} because {code_purple}{r}{code_reset} doesn't exist in the database.
                {code_green}Please verify your relations{code_reset}
                """)
    
    """
        Method called inside check_data(...).
        Used to check if the given attributes of a query exists within the given relations.
        @return True if everything is ok, raises ValueError if not.
    """
    def check_data_attributes(self):
        #checking the attributes within our relation:
        for a in self.attributes:                           #get our attributes
            if a.get_name() == "*":
                return True
            checker = False
            for ra in self.relations[0].attributes_list:    # get our relation's attributes
                if a.get_name() == ra.get_name():           # compare
                    checker=True

            if not checker:
                raise ValueError(f"""
                The (sub-)expression:
                | {str(self)} | is {code_red}invalid{code_reset} because the attribute {code_cyan}{a}{code_reset} doesn't exist within the given relation {code_purple}{self.relations[0]}{code_reset}.
                {code_green}Please verify your attributes{code_reset}
                """)
        

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
            attList.append(type_attribute_to_string_inside_expression(str(a),class_type_l))
        for r in self.relations:
            relList.append(type_attribute_to_string_inside_expression(str(r),class_type_l))

        attString = transform_list_to_goodString(attList)
        relString = transform_list_to_goodString(relList)

        return f'{wanted_expression} {attString} FROM {relString} {self.other_query_addons}'
        


    def __str__(self):
        return self.proper_str(self.class_type_list,self.SPJRUD_type)
        

# Tool Method
"""
    Method used to transform a list in proper string by stripping every paranthesis.
    @return String containing the content of the given list.
"""
def transform_list_to_goodString(myList):
    t0 = []
    for l in myList:
        t0.append(str(l))
    t = str(tuple(t0))
    if len(myList)== 1 :
            t = t[:len(t)-2]+")"

    t = t.replace("]","").replace("[","").replace("\"", "").replace(")","").replace("(","")
    return t


# Tool Method
# method that writes in sql format the given attribute
"""
    Method writing in sql format the given attribute.
    @return String of sql query.
"""
def type_attribute_to_string_inside_expression(myAttribute,class_type_list):

    if type(myAttribute) in class_type_list :
        return "( "+myAttribute.sql_query+" )"
    else:
        return str(myAttribute)


"""
    Class used to define Select query from SPJRUD format.
"""
class Select(Expression):

    def __init__(self,attributes_list,wanted_values_list,operation:str,relation):
        if len(attributes_list) != len(wanted_values_list):
            raise ValueError("Invalid number of attributes/wanted_values")
        # other_query_addons = self.create_query_addon(attributes_list,wanted_values_list,operation)
        
        super().__init__(attributes_list,[relation],"Select","Select")

        self.other_query_addons = self.create_query_addon(attributes_list,wanted_values_list,operation)

        self.accepted_operations = ["=",">","<",">=","<="]
        self.wanted_values_list = wanted_values_list
        self.operation = ""
        if operation.strip() not in self.accepted_operations:
            raise ValueError(f"Invalid operation {code_red}{operation}{code_reset} \n accepted operations : {code_green}{self.accepted_operations}{code_reset}")
        else:
            self.operation = operation.strip()

    '''
        Method used to create right part of a SQL query
        @return: in this exact case , it will return 'WHERE "Attribute" = "Value" '

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


"""
    Class used to define Project query from SPJRUD format.
"""
class Project(Expression):
    def __init__(self,attribute_list,relation):
        super().__init__(attribute_list,[relation],"Project","Select")


"""
    Class used to define Rename query from SPJRUD format.
"""
class Rename(Expression):
    def __init__(self, attribute_list, new_names_list:list[str],relation):
        self.new_names_list = new_names_list
        self.old_names_list = []
        for a in attribute_list:
            self.old_names_list.append(a.get_name())
        super().__init__(attribute_list,[relation],"Rename","ALTER TABLE")

    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self,data_base):

        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute()

        # create a "RENAME COLUMN old_name TO new_name" for each attribute
        rename_to_list = []
        x = 0
        while x < len(self.attributes):
            temp = f"RENAME COLUMN {self.attributes[x].get_name()} TO {self.new_names_list[x]}".replace("'","").replace("\"","")
            rename_to_list.append(temp)
            x+=1
        
        new_attributes = ",".join(rename_to_list)

        self.sql_query = f"{self.QUERY_TYPE} {relation.get_name()} {new_attributes};".replace("'","").replace("\\","")
        
        #change the names of the local attributes as well ! 
        x=0
        while x < len(self.attributes):
            self.attributes[x].name = self.new_names_list[x]
            x+=1

        return self.sql_query

    '''
        This method is used to create the string representation of this class.
        It uses a class_type_list since we're checking nested data within
        @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):

        old_att_name = []
        new_att_name = []
        rel_list = []

        for a in self.old_names_list:
            old_att_name.append(type_attribute_to_string_inside_expression(str(a),class_type_l))
        for a in self.new_names_list:
            new_att_name.append(type_attribute_to_string_inside_expression(str(a),class_type_l))
        for r in self.relations:
            rel_list.append(type_attribute_to_string_inside_expression(str(r),class_type_l))

        old_att_string = transform_list_to_goodString(old_att_name)
        new_att_string = transform_list_to_goodString(new_att_name)
        rel_string = transform_list_to_goodString(rel_list)

        return f'{wanted_expression} {old_att_string} TO {new_att_string} FROM {rel_string}'
       


"""
    Class used to define Join query from SPJRUD format.
"""
class Join(Expression):
    #TODO before joining check if the relations have commun atributes
    #so you don't fully join
    def __init__(self, relations_list):
        super().__init__([],relations_list,"Join","Union")
        for r in relations_list:
            if type(r) is not Relation:
                raise ValueError(f"""
                The (sub-)expression:
                | {str(self)} | is {code_red}invalid{code_reset} because {code_yellow}{r}{code_reset} is not a {code_purple}relation{code_reset}.
                {code_green}Please verify your relations{code_reset}
                """)
    
    def check_data(self, data_base):
        self.check_data_relations(data_base)
        
    
    # SPJRUD : Union R1,R2
    # SQL : (SELECT * FROM R) UNION (SELECT * FROM R)   

    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self,data_base):
        # TODO Before it saves itself to self.sql_query , DO THE CHECKING(from the db) + Error manager!!

        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute()
        
        if len(self.relations)== 2 :
            self.sql_query = f"(SELECT * FROM {str(self.relations[0])}) UNION (SELECT * FROM {str(self.relations[1])}) ".replace("'","").replace("\\","")
            return self.sql_query

        select_query_per_relation = []
        for relation in self.relations:
            select_query_per_relation.append(f"(SELECT * FROM {str(relation)})")

        self.sql_query = " UNION ".join(select_query_per_relation).replace("'","").replace("\\","")

        return self.sql_query
    

    '''        
        This method is used to create the string representation of this class.
    It uses a class_type_list since we're checking nested data within
     @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):
        # Prints the Expression as example: 
        # Select ['A0','A1'] from ["Relation"]

        relList = []

        for r in self.relations:
            relList.append(type_attribute_to_string_inside_expression(str(r),class_type_l))

        relString = transform_list_to_goodString(relList)

        return f'{wanted_expression} {relString} {self.other_query_addons}'

"""
    Class used to define Difference query from SPJRUD format.
"""
class Difference(Expression):
    def __init__(self, r1,r2):
        super().__init__([],[r1,r2],"Difference","Minus")
        temp = [r1,r2]
        for r in temp:
            if type(r) is not Relation:
                raise ValueError(f"""
                The (sub-)expression:
                | {str(self)} | is {code_red}invalid{code_reset} because {code_yellow}{r}{code_reset} is not a {code_purple}relation{code_reset}.
                {code_green}Please verify your relations{code_reset}
                """)
        self.r1 = r1
        self.r2 = r2
        
    def check_data(self, data_base):
        self.check_data_relations(data_base)

    # method transforming the SPJRUD expression to SQL expression
    # it checks if the attributes and relations are correct.
    def execute(self,data_base):
        # transforms the expression as SQL querry and saves it inside self.sql_query
        
        # TODO Before it saves itself to self.sql_query , DO THE CHECKING(from the db) + Error manager!!

        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)
        

        self.sql_query = f"({Project([Attribute('*','',True,True,[])],self.r1).execute(data_base)}) MINUS ({Project([Attribute('*','',True,True,[])],self.r2).execute(data_base)})".replace("'","").replace("\\","")

        return self.sql_query
    

    def proper_str(self,class_type_l,wanted_expression):
        # Prints the Expression as example: 
        # Select ['A0','A1'] from ["Relation"]

        return f'{wanted_expression} {transform_list_to_goodString(self.relations)} {self.other_query_addons}'


"""
    Class used to define Union query from SPJRUD format.
"""
class Union(Expression):
    # basically just Join but  R ∪ S is only allowed if R and S have exactly the same attributes

    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        temp = [r1,r2]
        for r in temp:
            if type(r) is not Relation:
                raise ValueError(f"""
                The (sub-)expression:
                | {str(self)} | is {code_red}invalid{code_reset} because {code_yellow}{r}{code_reset} is not a {code_purple}relation{code_reset}.
                {code_green}Please verify your relations{code_reset}
                """)
        super().__init__([],[r1,r2],"Union","Union")

    
    def execute(self,data_base):
        #check if r1,r2 have the EXACT same attributes
        # self.union_check_data(...)
        #execute Join([r1,r2])
        self.sql_query = Join([self.r1,self.r2]).execute(data_base)

        return self.sql_query
    
    # Overwrite -> def proper_str(self,class_type_l,wanted_expression)

    '''
        This method is used to create the string representation of this class.
        It uses a class_type_list since we're checking nested data within
        @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):
        well_written_str = transform_list_to_goodString(self.relations)
        return f'{wanted_expression} {well_written_str} '

 
