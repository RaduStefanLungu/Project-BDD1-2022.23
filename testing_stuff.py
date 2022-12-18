from classes.Requests import *
from classes.Attribute import Attribute
from classes.Relation import Relation
from classes.DataBase import DataBase

def testing_Expression_1():
    test = Expression(["A1","A2","A4"],["R"])
    print('\n')
    print(test)
    print('\n')
    print("executing -> "+test.execute())
    print("test.sql_query -> " + test.sql_query)
    print('\n')

def testing_Expression_2():
    expr0 = Expression(["E0","E1","E2"],["R0"])
    expr1 = Expression(["E3","E4","E5"],["R1"])
    test = Expression([expr0,"E10"],[expr1])

    print('\n')
    print(test)
    print('\n')
    print("executing -> "+test.execute())
    print("test.sql_query -> " + test.sql_query)
    print('\n')

    print('executing expr0 -> ' + expr0.execute())
    print('expr0.sql_query -> '+ expr0.sql_query)
    

def testing_Expression_3():
    a0 = Attribute("A0","numeric")
    a1 = Attribute("A1","TeXT")
    a2 = Attribute("A2","datE")
    a3 = Attribute("A3","NumERiC")
    
    print("\n")
    print(a0.get_info())
    print(a1.get_info())
    print(a2.get_info())
    print(a3.get_info())

    r0 = Relation("R0")
    r1 = Relation("R1")
    r2 = Relation("R2")

    expr0 = Expression([a0,a1],[r0],"Expression","Expression")
    expr1 = Expression([expr0,a2,a3],[r1],"Expression","Expression")
    print('\n\n')
    
    print(expr0)
    print(expr1)
    
    print('\n\n')

    print('\n\n')
    expr1.execute()
    print("expr1.execute().sql_query-->"+expr1.sql_query)
    print('\n\n')

def print_spjrud(e):
    print(f"SPJRUD : {e}")
def print_sql(e):
    print(f"SQL    : {e}")

def testing_Expression_4():

    a0 = Attribute("A0","TEXT",True,True,[])
    a1 = Attribute("A1","TEXT",True,True,[])
    a2 = Attribute("A2","INT",True,True,[])
    a3 = Attribute("A3","TEXT",True,True,[])
    a4 = Attribute("A4","TEXT",True,True,[])
    a5 = Attribute("A5","TEXT",True,True,[])
    a6 = Attribute("A6","TEXT",True,True,[])

    rel_1 = Relation("R1",[a0,a1,a2])
    rel_2 = Relation("R2",[a2,a3,a4])
    rel_3 = Relation("R3",[a5,a6])

    db = DataBase([rel_1,rel_2],"N/A")
    db.print_meta()
    # db.create_new_table("MyTableXXL",[a0,a1,a2])
    
    print("\n")


    t = Select([a0,a1],["Joe","Marry"],"=",rel_1)
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")

    t = Project([a0],rel_1)
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")

    t = Join([rel_1,rel_2])
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")

    t = Difference(rel_1,rel_2)
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")

    t = Union(rel_1,rel_2)
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")

    t = Rename([a0,a1],["custom0","custom1"],rel_1)
    t.execute(db)
    print_spjrud(t)
    print_sql(t.sql_query)
    print("\n")


def testing_SQLite_3():
    import sqlite3
    my_db = DataBase([],sqlite3.connect('./db/test.db'))
    my_db.fetch_data_from_connection()
    my_db.print_meta()

    e = Project([Attribute("*","",1,1,[])],my_db.get_relations()[0])
    e.execute(my_db)

    e1 = Select([Attribute("NAME","TEXT",1,1,[])],["Paul"],"=",my_db.get_relations()[0])
    e1.execute(my_db)

def testing_SQLite_2():
    import sqlite3

    conn = sqlite3.connect('./db/test.db')
    
    my_db = DataBase([],conn)
    my_db.fetch_data_from_connection()
    my_db.print_meta()

    # print(conn.execute('PRAGMA table_info("Company")').fetchall())

    for x in my_db.relations_list:
        print("-"+str(x))
        for a in x.attributes_list:
            print(a)

def testing_SQLite():
    import sqlite3

    conn = sqlite3.connect('./db/test.db')

    print("\nOpened database successfully!\n")


    """
    # conn.execute('''CREATE TABLE COMPANY
    #             (ID INT PRIMARY KEY     NOT NULL,    
    #             NAME TEXT               NOT NULL,
    #             AGE INT                 NOT NULL,
    #             ADDRESS CHAR(50)        NOT NULL,
    #             SALARY REAL);''')
    # print("table created successfully!\n")

    # conn.execute('''CREATE TABLE DEPARTMENTS
    #             (ID INT PRIMARY KEY     NOT NULL,    
    #             NAME TEXT               NOT NULL,
    #             ADDRESS CHAR(50)        NOT NULL);''')
    # print("table created successfully!\n")



    # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

    # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

    # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

    # conn.commit()


    # conn.execute("INSERT INTO DEPARTMENTS (ID,NAME,ADDRESS) \
    #       VALUES (1, 'IT', 'Mons' )");

    # conn.execute("INSERT INTO DEPARTMENTS (ID,NAME,ADDRESS) \
    #       VALUES (2, 'Marketing', 'Charleroi' )");

    # conn.execute("INSERT INTO DEPARTMENTS (ID,NAME,ADDRESS) \
    #       VALUES (3, 'Secretary', 'Mons' )");


    # conn.commit()


    # cursor = conn.execute("SELECT id,name,age,address,salary from COMPANY")
    """

    my_db = DataBase([],conn)

    x = Project(["id","name","age","address","salary"],"COMPANY")
    y = Project(["id","name","salary"],x)

    relation = x
    relation.execute(my_db)
    print(relation)
    print(relation.sql_query)
    print("""
            Enter yes to execute query.\n
            Enter no to stop\n
        """)
    answear = input("---->>> ")

    cursor = None
    if answear == "yes" or answear=="y":
        cursor = conn.execute(relation.get_sql_query())  
    else:
        return -1


    relation_att = []
    print("--- Attributes of relation:\n")
    for column in cursor.description:
        relation_att.append(column[0])
        print(column[0])
    print('\n---\n')

    cursor_data =cursor.fetchall() 
    print("-Cursor had been empties with values inside cursor_data-")
    for t in cursor_data:
        counter = 0
        while counter < len(t):
            print(f"{relation_att[counter]} : {t[counter]}")
            counter += 1 
        print("\n")




    for row in cursor:
        print("ID = "+ str(row[0]))
        print("Name = "+ str(row[1]))
        print("Age = "+ str(row[2]))
        print("Address = "+ str(row[3]))
        print("Salary = "+ str(row[4]))
        print("\n")

    

    print("Operation done successfully!\n")

    print("\n--- Relations of the DataBase:")
    cursor = conn.cursor()
    cursor.execute("SELECT (name) FROM sqlite_master WHERE type='table';")
    tableList = cursor.fetchall()
    print(tableList)
    print('\n---\n')

    conn.close()



if __name__=='__main__':
    print("\n-----START-----\n")

    # testing_SQLite_3()
    # testing_Expression_4()

    # import sqlite3
    # conn = sqlite3.connect('./db/test.sqlite')

    # # conn.execute('''CREATE TABLE EMPLOYEES
    # #             (ID INT PRIMARY KEY     NOT NULL,    
    # #             NAME TEXT               NOT NULL,
    # #             EMAIL TEXT                 NOT NULL,
    # #             HOME_ADDRESS CHAR(50)        NOT NULL);''')
    # # print("table created successfully!\n")

    # conn.execute("INSERT INTO EMPLOYEES (ID,NAME,EMAIL,HOME_ADDRESS) \
    #       VALUES (1, 'Paul','paul_gica@gmail.com', 'Rue de la Tombe 20')");
    # conn.execute("INSERT INTO EMPLOYEES (ID,NAME,EMAIL,HOME_ADDRESS) \
    #       VALUES (2, 'Allen','allen_maiden@gmail.com', 'Rue de la MishMish 1')");
    # conn.execute("INSERT INTO EMPLOYEES (ID,NAME,EMAIL,HOME_ADDRESS) \
    #       VALUES (3, 'Teddy','teddy_the_bear@hotmail.com', 'Avenue du Miel 99')");
    # conn.execute("INSERT INTO EMPLOYEES (ID,NAME,EMAIL,HOME_ADDRESS) \
    #       VALUES (4, 'Mark','mark_le_camataire@yahoo.com', 'Rue de ouest 45')");
    # conn.commit()

    print("\n------END------\n")












