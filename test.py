from classes.Expression import Expression

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
    



if __name__=='__main__':
    
    testing_Expression_2()