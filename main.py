from classes.Attribute import Attribute
from classes.Relation import Relation
from classes.Requests import *
from classes.DataBase import DataBase


def main():
    import sqlite3

    # example of usage:
    file_path = './db/test.db'
    my_db = DataBase(sqlite3.connect(file_path))
    my_db.fetch_data_from_connection()              # fill the DataBase object with data from .db file
    my_db.print_meta()                              # visual of the whole db

    # examples of SPRJUD algebra used on this db :

                 #creating an * attribute   | 
                 #to select data from table | #since we need here a relation to work on, we get that from the DataBase obj.                 
    e0 = Project([Attribute("*","",1,1,[])],my_db.get_relations()[0])
    e00 = Project([Attribute("*","",1,1,[])],my_db.get_relations()[1])
    #let's turn that SPRJUD expression to a sql expression:
    e0.execute(my_db)
    e00.execute(my_db)
    # If you want to visualise the SPRJUD expression just use print(e0)
    # Keep in mind that you won't be able to see the sql expression
    # if you haven't used the .execute(db) method.
    # After execution you can use e0.sql_query to visualise the transformed query.
    print("\nOld query : "+str(e0))                 # -> this prints the SPRJUD expression
    print("\nTransformed query : "+e0.sql_query+"\n")    # -> this prints the SQL expression
    #
    # To apply the query on the wanted Data Base, you need to execute the execute_on_db(my_db) method
    e0.execute_on_db(my_db)
    e00.execute_on_db(my_db)
    #
    # Various errors exist, let me show you one here (uncomment the next 2 lines):
    # e1 = Union(my_db.get_relations()[0],Attribute("ADDRESS","TEXT",1,1,[]))
    # e1.execute(my_db)       # <-- this will give us an error
    #
    #
    # You can even use composed querries:
    e20 = Project([Attribute("SALARY","TEXT",0,1,[])],my_db.get_relations()[0])
    e21 = Project([Attribute("NAME","TEXT",0,1,[]),Attribute("ADDRESS","TEXT",0,1,[])],my_db.get_relations()[1])
    e2 = Union(e20,my_db.get_relations()[1])
    e2.execute(my_db)
    print(e2.sql_query)
    e2.execute_on_db(my_db)

if __name__=='__main__':
    print("\n-----START-----\n")

    main()

    print("\n------END------\n")