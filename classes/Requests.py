from classes.Relation import Relation
from classes.Attribute import Attribute
from classes.CustomErrors import *


#### Tool Methods ####

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
    #TODO CHANGED HERE !!!!!
    t = t.replace("]","").replace("[","").replace("\"", "").replace(")","").replace("(","").replace("<","(").replace(">",")")
    return t

"""
    Method writing in sql format the given attribute.
    @return String of sql query.
"""
def type_attribute_to_string_inside_expression(myAttribute,class_type_list):

    if type(myAttribute) in class_type_list :
        return "( "+myAttribute.sql_query+" )"
    else:
        return str(myAttribute)


######################

"""
    Parent class defining SPRJUD expressions.
"""
class Expression(object):
    
    def __init__(self,attribute_list,relation_list,SPJRUD_type:str,QUERY_TYPE:str):
        self.attributes = attribute_list
        self.relations = relation_list
        self.SPJRUD_type:str = SPJRUD_type
        self.QUERY_TYPE:str = QUERY_TYPE    # example : Select/Project/Join etc.
        self.other_query_addons = ""        # ment to be changed manually due to function order calls.
        self.sql_query = "- ! You forgot to use execute() method ! -"     # ment to be send to SQLite DB after usage of execute()
        self.class_type_list = [Expression,Select,Project,Rename,Join,Difference,Union] # list of children class types * MUST BE UPDATED FOR EVERY NEW CHILDREN IN THE CODE ! *
    

    """
        Method used to transform the SPJRUD expression to SQL expression and doing all the needed checking beforehand on the expression.
        When completed, this method will execute the right query on the given data base.
        To acess that query use <expression>.get_sql_query().
    """
    def execute(self,data_base):
        self.check_data(data_base)

        for attribute in self.attributes:
            if type(attribute) in self.class_type_list:
                attribute.execute(data_base)
        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)


        #TODO CHANGED HERE !!
        self.sql_query = self.proper_str(self.class_type_list,self.QUERY_TYPE).replace("\\","")

        return self.sql_query


    '''
        This method is used to create the string representation of this class.
        It uses a class_type_list since we're checking nested data within
        @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):

        attList = []
        relList = []

        for a in self.attributes:
            attList.append(type_attribute_to_string_inside_expression(str(a),class_type_l))

        #TODO CHANGED HERE !!
        for r in self.relations:
            #TODO CHANGED HERE !!!!!
            if type(r) in self.class_type_list:
                relList.append(f"<{type_attribute_to_string_inside_expression(r.sql_query,class_type_l)}>")
            else:
                relList.append(type_attribute_to_string_inside_expression(str(r),class_type_l))

        attString = transform_list_to_goodString(attList)
        relString = transform_list_to_goodString(relList)


        #TODO CHANGED HERE !!
        left_side_query = f'{wanted_expression} {attString} FROM {relString}'.replace("'","")
        return f"{left_side_query}{self.other_query_addons}"
        


    """
        Method that will execute the  sql query on the given data base.
    """
    def execute_on_db(self,db):
        db.execute_query(self.sql_query)

    '''
        This method verifies if entered data as SPJRUD query is correct and if it checks within the database.
    '''
    def check_data(self,data_base):
        
        self.check_data_relations(data_base)
        # self.check_data_attributes()
        pass
        
    """
        Method called inside check_data(...).
        Used to check if the given relations of a query exists within the data base.
        @return True if everything is ok, raises ValueError if not.
    """
    def check_data_relations(self,data_base):
        for r in self.relations:
            if type(r) is not Relation and (type(r) is not self.class_type_list):
                raise InvalidRelationType(self,r)
            exist_in_db = False
            for db_r in data_base.get_relations():
                if db_r.get_name() is r.get_name():
                    exist_in_db=True
            
            if not exist_in_db:
                raise RelationNotInDBError(self,r.get_name())
        
        return 1
        for r in self.relations:
            if type(r) in self.class_type_list and r.get_name() not in data_base.relations_list_name:
                raise RelationNotInDBError(self,r.get_name())
    
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
                raise AttributeNotInRelationError(self,a)
        

    def get_sql_query(self):
        return self.sql_query

    def __str__(self):
        return self.proper_str(self.class_type_list,self.SPJRUD_type)
        



"""
    Class used to define Select query from SPJRUD format.
"""
class Select(Expression):

    def __init__(self,attributes_list,wanted_attribute_list,operation:str,wanted_values_list,relation):
        if len(wanted_attribute_list) != len(wanted_values_list):
            raise InvalidNumberOfVariablesError("attributes/wanted values")
        
        super().__init__(attributes_list,[relation],"Select","SELECT")

        self.other_query_addons = self.create_query_addon(wanted_attribute_list,wanted_values_list,operation)
        self.accepted_operations = ["=",">","<",">=","<="]
        self.wanted_attribute_list = wanted_attribute_list
        self.wanted_values_list = wanted_values_list
        self.operation = ""
        if operation.strip() not in self.accepted_operations:
            raise InvalidOperationError(operation,self.accepted_operations)
        else:
            self.operation = operation.strip()

    '''
        Method used to create right part of a SQL query
        @return: in this exact case , it will return 'WHERE "Attribute" = "Value" '

    '''
    def create_query_addon(self,wanted_att,wanted_values,operation:str):
        query_addon = " WHERE "
        left_constructor = []
        types_list = self.class_type_list
        x = 0
        while x < len(wanted_att):
            if type(wanted_att[x]) in types_list:
                if type(wanted_values[x])== str:
                    temp = "("+str(wanted_att[x])+")" + operation + "'"+wanted_values[x]+"'"
                else:
                    temp = "("+str(wanted_att[x])+")" + operation + str(wanted_values[x])
            else : 
                if type(wanted_values[x])== str:
                    temp = str(wanted_att[x]) + operation + "'"+wanted_values[x]+"'"
                else:
                    temp = str(wanted_att[x]) + operation + str(wanted_values[x])
            
            
            left_constructor.append(temp)
            x += 1

        query_addon += ' and '.join(left_constructor)

        return query_addon


"""
    Class used to define Project query from SPJRUD format.
"""
class Project(Expression):
    def __init__(self,attribute_list,relation):
        super().__init__(attribute_list,[relation],"Project","SELECT DISTINCT")


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

    """
        Method used to transform the SPJRUD expression to SQL expression and doing all the needed checking beforehand on the expression.
        When completed, this method will execute the right query on the given data base.
        To acess that query use <expression>.get_sql_query().
    """
    def execute(self,data_base):

        self.check_data(data_base)
        self.check_attributes_name_or_type()

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)

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

    """
        Method checking if the newly named attributes respect data types.
        @return True if the data types are respected
    """
    def check_attributes_name_or_type(self):
        def get_attribute_by_name(n,attribute_list):
            for a in attribute_list:
                if a.get_name() == n:
                    return a
        def get_all_names_from_attributes(a_list):
            my_names = []
            for a in a_list:
                my_names.append(a.get_name())
            return my_names

        all_attributes_names = get_all_names_from_attributes(self.relations[0].get_attributes_list())

        for index in range(len(self.new_names_list)):
            if self.new_names_list[index] in all_attributes_names:
                if get_attribute_by_name(self.old_names_list[index],self.attributes).get_data_type() != get_attribute_by_name(self.new_names_list[index],self.relations[0].get_attributes_list()).get_data_type():
                    raise InvalidNewAttributeTypeOnNameChangeError(get_attribute_by_name(self.old_names_list[index],self.attributes),get_attribute_by_name(self.new_names_list[index],self.relations[0].get_attributes_list()))
        return True


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
    def __init__(self, relations_list):
        super().__init__([],relations_list,"Join","CROSS JOIN")
    
    def check_data(self, data_base):
        self.check_data_relations(data_base)
    
    def check_data_join(self):
        #TODO check # of attributes etc. etc. etc.
        pass

    """
        Method used to transform the SPJRUD expression to SQL expression and doing all the needed checking beforehand on the expression.
        When completed, this method will execute the right query on the given data base.
        To acess that query use <expression>.get_sql_query().
    """
    def execute(self,data_base):
        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)
        
        self.check_data_join()

        if len(self.relations)== 2 :
            all_halvs_of_query = []
            for relation in self.relations:
                if type(relation) in self.class_type_list:
                    all_halvs_of_query.append(f"({relation.sql_query})")
                else:
                    all_halvs_of_query.append(f"SELECT * FROM {relation.get_name()}")

            self.sql_query = " CROSS JOIN ".join(all_halvs_of_query).replace("'","").replace("\\","")
            return self.sql_query

        else:
            select_query_per_relation = []
            for relation in self.relations:
                if type(relation) in self.class_type_list:
                    select_query_per_relation.append(f"({relation.sql_query})")    
                else:
                    select_query_per_relation.append(f"SELECT * FROM {relation.get_name()}")

            self.sql_query = " CROSS JOIN ".join(select_query_per_relation).replace("'","").replace("\\","")

            return self.sql_query
    

    '''        
        This method is used to create the string representation of this class.
    It uses a class_type_list since we're checking nested data within
     @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):
        relList = []

        for r in self.relations:
            #TODO CHANGED HERE !!!!!
            if type(r) in self.class_type_list:
                relList.append(f"<{type_attribute_to_string_inside_expression(r.sql_query,class_type_l)}>")
            else:
                relList.append(type_attribute_to_string_inside_expression(str(r),class_type_l))



        relString = transform_list_to_goodString(relList)

        return f'{wanted_expression} {relString} {self.other_query_addons}'

"""
    Class used to define Difference query from SPJRUD format.
"""
class Difference(Expression):
    def __init__(self, r1,r2):
        super().__init__([],[r1,r2],"Difference","EXCEPT")
        temp = [r1,r2]
        for r in temp:
            if type(r) is not Relation and type(r) not in self.class_type_list:
                raise InvalidRelationType(self,r)
        self.r1 = r1
        self.r2 = r2
        
    def check_data(self, data_base):
        self.check_data_relations(data_base)

    """
        Method used to transform the SPJRUD expression to SQL expression and doing all the needed checking beforehand on the expression.
        When completed, this method will execute the right query on the given data base.
        To acess that query use <expression>.get_sql_query().
    """
    def execute(self,data_base):

        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)
        
        halves_of_query = []
        
        for r in self.relations:
            if type(r) in self.class_type_list:
                halves_of_query.append(r.sql_query)
            # here we know that it can only be type Relation:
            else:
                halves_of_query.append(f"SELECT * FROM {r.get_name()}")

        self.sql_query = f" {self.QUERY_TYPE} ".join(halves_of_query)
        #.replace("\\","")

        return self.sql_query
    

    def proper_str(self,class_type_l,wanted_expression):
        return f'{wanted_expression} {transform_list_to_goodString(self.relations)} {self.other_query_addons}'


"""
    Class used to define Union query from SPJRUD format.
"""
class Union(Expression):
    # basically just Join but  R ∪ S is only allowed if R and S have exactly the same attributes(name,type)

    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        temp = [r1,r2]
        super().__init__([],[r1,r2],"Union","UNION")
        

    def check_data_union(self):
        # r1 is expression
        if type(self.r1) in self.class_type_list:
            # r2 is expression
            if type(self.r2) in self.class_type_list:
                r1_att_name = []
                r1_att_type = []
                for a1 in self.r1.attributes:
                    r1_att_name.append(a1.get_name())
                    r1_att_type.append(a1.get_data_type())

                for a2 in self.r2.attributes:
                    if a2.get_name() not in r1_att_name:
                        raise AttributesNameDontMatchError(a2.get_name())
                    if a2.get_data_type() not in r1_att_type:
                        raise AttributesTypeDontMatchError(a2.get_data_type())
            # r2 is not expression
            else:
                r1_att_name = []
                r1_att_type = []
                for a1 in self.r1.attributes:
                    r1_att_name.append(a1.get_name())
                    r1_att_type.append(a1.get_data_type())

                for a2 in self.r2.get_attributes_list():
                    if a2.get_name() not in r1_att_name:
                        raise AttributesNameDontMatchError(a2.get_name())
                    if a2.get_data_type() not in r1_att_type:
                        raise AttributesTypeDontMatchError(a2.get_data_type())
        # r1 is not expression
        else:
            # r2 is expression
            if type(self.r2) in self.class_type_list:
                r1_att_name = []
                r1_att_type = []
                for a1 in self.r1.get_attributes_list():
                    r1_att_name.append(a1.get_name())
                    r1_att_type.append(a1.get_data_type())

                for a2 in self.r2.attributes:
                    if a2.get_name() not in r1_att_name:
                        raise AttributesNameDontMatchError(a2.get_name())
                    if a2.get_data_type() not in r1_att_type:
                        raise AttributesTypeDontMatchError(a2.get_data_type())
            # r2 is not expression
            else:
                r1_att_name = []
                r1_att_type = []
                for a1 in self.r1.get_attributes_list():
                    r1_att_name.append(a1.get_name())
                    r1_att_type.append(a1.get_data_type())

                for a2 in self.r2.get_attributes_list():
                    if a2.get_name() not in r1_att_name:
                        raise AttributesNameDontMatchError(a2.get_name())
                    if a2.get_data_type() not in r1_att_type:
                        raise AttributesTypeDontMatchError(a2.get_data_type())

    """
        Method used to transform the SPJRUD expression to SQL expression and doing all the needed checking beforehand on the expression.
        When completed, this method will execute the right query on the given data base.
        To acess that query use <expression>.get_sql_query().
    """
    def execute(self,data_base):

        self.check_data(data_base)

        for relation in self.relations:
            if type(relation) in self.class_type_list:
                relation.execute(data_base)
        
        #TODO CHANGED HERE !!
        self.check_data_union()

        elements = []
        for relation in self.relations:
            if type(relation) in self.class_type_list:
                elements.append(f"{relation.sql_query}")
            else:
                elements.append(f"{relation.get_name()}")
        self.sql_query = f" {self.QUERY_TYPE} ".join(elements).replace("\\","")

        return self.sql_query

    '''
        This method is used to create the string representation of this class.
        It uses a class_type_list since we're checking nested data within
        @return String containing the wanted_expression type (SPJRUD_type or QUERY_TYPE->SQL)
    '''
    def proper_str(self,class_type_l,wanted_expression):
        well_written_str = transform_list_to_goodString(self.relations)
        return f'{wanted_expression} {well_written_str} '

 
