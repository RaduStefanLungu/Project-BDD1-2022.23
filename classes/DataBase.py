from classes.Relation import Relation
from classes.Attribute import Attribute

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
    attribute_text_prefix = "++++++++ "

    def __init__(self,sqlite_connection):
        self.relations_list = []
        self.relations_list_name = []
        self.connection = sqlite_connection
        self.fill_relations_list_name()

    def get_relations(self):
        return self.relations_list

    def get_connection(self):
        return self.connection

    """
        Method used to fill DataBase object with data from a given connection.
        It will overwrite existing relations within the object.
        ! To be used only if you want to fetch data from a sql connection (e.g. SQLite) !
    """
    def fetch_data_from_connection(self):
        #TODO
        if self.connection != None :
            db_rel = []
            #get all table names
            db_rel_table = self.connection.cursor().execute("SELECT (name) FROM sqlite_master WHERE type='table';").fetchall()
            #get relation name from db
            for t in db_rel_table:
                db_rel.append(t[0])
            #create relations objects
            for r in db_rel:
                self.relations_list.append(Relation(r,[]))

            #get all tables' attributes:
            for rel in self.relations_list:
                full_data_db = self.connection.cursor().execute(f"PRAGMA table_info('{rel.get_name()}')").fetchall()
                for info in full_data_db:
                    rel.attributes_list.append(Attribute(info[1],info[2],info[5],info[3],[]))

            self.fill_relations_list_name()
        else:
            raise ConnectionError("Connection is not established with the database.")

    def fill_relations_list_name(self):
        for r in self.relations_list:
            self.relations_list_name.append(r.get_name())

    """
        Method used to execute the given query on the saved connection.
        @return inserted query.
    """
    def execute_query(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        print(f"{self.db_text_prefix}{code_green}execute_query({query}) had been successfully executed{code_reset}")
        self.print_executed_query(cursor)
        return(query)

    def print_executed_query(self,cursor):
        tab = cursor.fetchall()
        data = []
        for el in tab :
            data.append(str(el))
        
        print("\n".join(data))

    """
        Method used to print the data about this data base object.
        Basically it prints the data base's relations and attributes info.
    """
    def print_meta(self):
        prints = []
        for r in self.relations_list:
            l = []
            l.append(f"{self.relation_text_prefix}{r.get_name()}")
            for a in r.attributes_list:
                l.append(f"{self.attribute_text_prefix}{a.get_info()}")
            prints.append("\n".join(l))

        p ="\n\n".join(prints) 
        s = f"""
{self.db_text_prefix}This DataBase contains the following relations and attributes :

{p}"""
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
        #TODO
        pass