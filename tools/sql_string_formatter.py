from classes.Expression import Expression

# since if you do str(tuple(["R"])) we get ("R",) we had to remove the "," at the end 
# it only happens when there is only one element in the list.
def transform_list_to_goodString(myList):
    t = str(tuple(myList))
    if len(myList)== 1 :
            t = t[:len(t)-2]+")"

    t = str(myList)
    t = t.replace("\"", "")
    t = t.replace("]","").replace("[","")
    return t


# method that writes in sql format the given attribute
def type_attribute_to_string_inside_expression(myAttribute):
    if type(myAttribute) == Expression:
        return "("+str(myAttribute)+")"
    else:
        return str(myAttribute)
        

