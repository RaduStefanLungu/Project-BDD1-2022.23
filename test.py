from classes.Expression import Expression
from classes.Attribute import Attribute
from classes.Relation import Relation

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

    expr0 = Expression([a0,a1],[r0])
    expr1 = Expression([expr0,a2,a3],[r1])
    print('\n\n')
    
    print(expr0)
    print(expr1)
    
    print('\n\n')

    print('\n\n')
    expr1.execute()
    print("expr1.execute().sql_query-->"+expr1.sql_query)
    print('\n\n')

def testing_SQLite():
    import sqlite3

    conn = sqlite3.connect('./db/test.db')

    print("\nOpened database successfully!\n")



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


    cursor = conn.execute("SELECT id,name,age,address,salary from COMPANY")


    for row in cursor:
        print("ID = "+ str(row[0]))
        print("Name = "+ str(row[1]))
        print("Age = "+ str(row[2]))
        print("Address = "+ str(row[3]))
        print("Salary = "+ str(row[4]))
        print("\n")

    print("--- Attributes of COMPANY relation:\n")
    for column in cursor.description:
        print(column[0])
    print('\n---\n')

    print("Operation done successfully!\n")

    print("\n--- Relations of the DataBase:")
    cursor = conn.cursor()
    cursor.execute("SELECT (name) FROM sqlite_master WHERE type='table';")
    tableList = cursor.fetchall()
    print(tableList)
    print('\n---\n')

    conn.close()



if __name__=='__main__':
    
    testing_Expression_3()
    testing_SQLite()














