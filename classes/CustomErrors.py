
#Colors taken from AINSI CODE from : https://www.geeksforgeeks.org/print-colors-python-terminal/

code_reset = "\033[00m"
code_red = "\033[91m"
code_green = "\033[92m"
code_yellow = "\033[93m"
code_light_purple = "\033[94m"
code_purple = "\033[95m"
code_cyan = "\033[96m"
code_light_gray = "\033[97m"

class RelationNotInDBError(Exception):

    def __init__(self, expression,relation):
        self.message = f"""
        The (sub-)expression:
        | {str(expression)} | is {code_red}invalid{code_reset} because {code_purple}{relation}{code_reset} doesn't exist in the database.
        {code_green}Please verify your relations.{code_reset}
        """
    
    def __str__(self):
        return self.message

class InvalidRelationType(Exception):
    
    def __init__(self, expression,invalid_relation):
        self.message = f"""
                The (sub-)expression:
                | {str(expression)} | is {code_red}invalid{code_reset} because {code_yellow}{invalid_relation}{code_reset} is not a {code_purple}relation{code_reset}.
                {code_green}Please verify your relations{code_reset}
                """
    
    def __str__(self):
        return self.message


class AttributeNotInRelationError(Exception):

    def __init__(self, expression, attribute):
        self.message = f"""
                The (sub-)expression:
                | {str(expression)} | is {code_red}invalid{code_reset} because the attribute {code_cyan}{attribute}{code_reset} doesn't exist within the given relation {code_purple}{expression.relations[0]}{code_reset}.
                {code_green}Please verify your attributes{code_reset}
                """
    def __str__(self):
        return self.message


class InvalidNumberOfVariablesError(Exception):

    def __init__(self,invalid_type_of_variable):
        self.message = f"""
        {code_red}Invalid{code_reset} number of {invalid_type_of_variable}.
        {code_green}Please check your values.{code_reset}"""

    def __str__(self):
        return self.message

class InvalidOperationError(Exception):
    
    def __init__(self,invalid_operation,accepted_operations):
        self.message = f"""
        {code_red}Invalid{code_reset} operation '{code_red}{invalid_operation}{code_reset}'.
        {code_green}Accepted{code_reset} operations : {code_green}{accepted_operations}{code_reset}
        """

    def __str__(self):
        return self.message

class InvalidNewAttributeTypeOnNameChangeError(Exception):
    
    def __init__(self,new_named_attribute,existent_attribute):
        self.message = f"""
        {code_red}Invalid{code_reset} newly named attribute type.
        Newly named attribute type      = {code_light_purple}{new_named_attribute.get_data_type()}{code_reset}
        Already existent attribute type = {code_light_purple}{existent_attribute.get_data_type()}{code_reset}
        {code_green}Please check your attributes types.{code_reset}
        """

    def __str__(self):
        return self.message


class AttributesNameDontMatchError(Exception):
    
    def __init__(self,att_name1):
        self.message = f"""
        {code_red}Invalid{code_reset} attribute name.
        Bad attribute name : {code_light_purple}{att_name1}{code_reset}
        {code_green}Please check your attributes types.{code_reset}
        """

    def __str__(self):
        return self.message

class AttributesTypeDontMatchError(Exception):
    
    def __init__(self,att_type1):
        self.message = f"""
        {code_red}Invalid{code_reset} attribute type.
        Bad attribute type : {code_light_purple}{att_type1}{code_reset}
        {code_green}Please check your attributes types.{code_reset}
        """

    def __str__(self):
        return self.message