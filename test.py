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

if __name__=='__main__':
    
    testing_Expression_3()