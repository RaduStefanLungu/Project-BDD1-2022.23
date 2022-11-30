
class DataBase(object):
    db_text_prefix = ">> "
    relation_text_prefix = ">>>> "

    def __init__(self,relations_list,sqlite_connection):
        self.relations_list = relations_list
        self.relations_list_name = []
        self.connection = sqlite_connection
        for r in self.relations_list:
            self.relations_list_name.append(r.get_name())

    def print_meta(self):
        relations = []
        for rel in self.relations_list:
            relations.append(rel.get_name())
        relations_str = f'\n{self.relation_text_prefix}'.join(relations)
        s = f"{self.db_text_prefix}This DataBase contains the follow relations : \n{self.relation_text_prefix}{relations_str}"
        print(s)

    def __str__(self):
        pass