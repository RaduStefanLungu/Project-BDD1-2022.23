from classes.Attribute import Attribute
from classes.Relation import Relation
from classes.Requests import *
from classes.DataBase import DataBase


# Vous pouvez uncommenter certains bloques pour voir le résultat sur la database d'exemple

if __name__=='__main__':
    print("\n-----START-----\n")

    # main()
    import sqlite3
    my_db = DataBase(sqlite3.connect('./db/test.sqlite'))
    my_db.fetch_data_from_connection()

    my_db.print_meta()


    company = my_db.get_relations()[0]
    departments = my_db.get_relations()[1]
    employees = my_db.get_relations()[2]

    all = Attribute("*","TEXT",0,0,[])
    q0 = Project([all],employees)
    q0.execute(my_db)
    q0.execute_on_db(my_db)

    att_salary = Attribute("SALARY","TEXT",0,0,[])
    q1 = Select([att_salary],"=",[20000],company)
    q1.execute(my_db)
    print(q1.sql_query)
    q1.execute_on_db(my_db)

    att_salary = Attribute("SALARY","TEXT",0,0,[])
    att_address = Attribute("ADDRESS","TEXT",0,0,[])
    att_name = Attribute("NAME","TEXT",0,0,[])
    q11 = Select([att_name],"=",["Paul"],q1)
    # q11.execute(my_db)
    # print(q11.sql_query)
    # q11.execute_on_db(my_db)


    # print("\n")
    # att_ = Attribute("NAME","TEXT",0,0,[])
    # q2 = Project([att_salary],q1)
    # q2.execute(my_db)
    # print(q2.sql_query)
    # q2.execute_on_db(my_db)


    print("\n\n")

    att_ = Attribute("NAME","TEXT",0,0,[])
    q2 = Join(departments,q1)
    q2.execute(my_db)
    print(q2.sql_query)
    q2.execute_on_db(my_db)


    # print("\n\n")

    # r1 = Select([all],[att_salary],">",[20000],company)
    # r2 = Select([all],[att_name],"=",["Paul"],company)
    # q2 = Union(r1,r2)
    # q2.execute(my_db)
    # print(q2.sql_query)
    # q2.execute_on_db(my_db)

#   Error example of Relation not in DB: 

    # print("\n\n")

    # r1 = Select([all],[att_salary],">=",[20000],company)
    # r2 = Select([all],[att_name],"=",["Paul"],company)
    # q2 = Difference(company,Relation("JINX",[att_salary,att_name]))
    # q2.execute(my_db)
    # print(q2.sql_query)
    # q2.execute_on_db(my_db)
    
#   -------

    # print('\n\n')

    # cursor = my_db.connection.cursor()
    # cursor.execute("SELECT * FROM company WHERE salary>=20000 EXCEPT SELECT * FROM company WHERE name='Paul'")
    # print(cursor.fetchall())

    # print("\n------END------\n")

