#defining something something

# TODO: you'll have to turn each of these in objects , extended from <Expr> class(parent class)
# You have to print error message based on the type of error(wrong attribute type etc...)
# You have to print the tables on the screen from the db (SQLite) 
# [...]


# All these function have to return a SQL query (string most likly)


def Project(attribute_list:list[str],table_name:str):
    # example : Project(["A","B"])
    # SQL : SELECT A, B FROM R

    # Since relations are sets, duplicates are removed.
    pass

def Select(table_name:str,attribute:str,operation:str,wanted_value):
    # example : Select(R,A,"=",1)
    # SQL : SELECT * FROM R WHERE A="1"
    pass


def Join(table_name_1:str,table_name_2:str):
    # example : Join("R","S")
    # SQL : SELECT * FROM R, S

    # R on S contains all tuples t such that t[ABC] is in R, and t[BCD] in S.
    pass
def Rename(table_name:str,attribute_old_name:str,attribute_new_name:str):
    # SQL : ???
    pass
def Union(table_name_1:str,table_name_2:str):
    # example : Union("R","S")
    # SQL : (SELECT * FROM R) UNION (SELECT * FROM S)

    # R ∪ S is only allowed if R and S have exactly the same attributes
    pass
def Difference(table_name_1:str,table_name_name_2:str):
    # example : Difference("R","S")
    # SQL : (SELECT * FROM R) MINUS (SELECT * FROM S)

    # R − S is only allowed if R and S have exactly the same attributes
    pass


# Project <- [Select,Join,Union,Difference]
