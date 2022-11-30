from classes.Relation import Relation

code_reset = "\033[00m"
code_red = "\033[91m"
code_green = "\033[92m"
code_yellow = "\033[93m"
code_light_purple = "\033[94m"
code_purple = "\033[95m"
code_cyan = "\033[96m"
code_light_gray = "\033[97m"


class DataBase(object):
    db_text_prefix = ">> "
    relation_text_prefix = ">>>> "

    def __init__(self,relations_list,sqlite_connection):
        self.relations_list = relations_list
        self.relations_list_name = []
        self.connection = sqlite_connection
        for r in self.relations_list:
            self.relations_list_name.append(r.get_name())

    """
        Method used to execute the given query on the saved connection.
        @return inserted query.
    """
    def execute_query(self,query):
        self.connection.execute(query)
        print(f"{self.db_text_prefix}{code_green}execute_query(.) had been successfully executed{code_reset}")
        return(query)

    def print_meta(self):
        relations = []
        for rel in self.relations_list:
            relations.append(rel.get_name())
        relations_str = f'\n{self.relation_text_prefix}'.join(relations)
        s = f"{self.db_text_prefix}This DataBase contains the follow relations : \n{self.relation_text_prefix}{relations_str}"
        print(s)

    def create_table_as(self):
        #TODO
        pass

    def create_new_table(self,table_name,attributes_list):
        attributes = ""
        a_name_list = []
        for a in attributes_list:
            temp = a.get_name() + " " + a.get_data_type()
            if a.primary_key:
                temp += " PRIMARY KEY "
            if a.not_null:
                temp += " NOT NULL "
            a_name_list.append(temp)
        attributes = ",".join(a_name_list).replace("\"","").replace("'","")


        creational_query = f"CREATE TABLE {table_name} ({attributes});"

        self.connection.execute(creational_query)
        print(f"{self.db_text_prefix}{code_green}New relation/table <{table_name}> has been successfully created{code_reset}")
        self.relations_list.append(Relation(table_name,attributes_list))

    def __str__(self):
        pass