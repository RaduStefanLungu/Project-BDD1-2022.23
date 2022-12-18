# Tutoriel : comment utiliser cette librarie.

>> Il est essentiel pour l'usage de cette librarie d'utiliser sqlite3.

>> Pour utiliser cetter librarie il faut importer les classes du fichier ./classes/Requests.py
    (from classes.Requests import *) et aussi il faut importer la classe DataBase pour
    pouvoir appliquer les requêtes sur le fichier .db ou .sqlite désiré.
    (from classes.DataBase import DataBase) De plus il faut importer la classe Attribute et
    Relation.(  from classes.Attribute import Attribute
                from classes.Relation import Relation   )

Voici un example d'utilisation en code : 

>import sqlite3
>from classes.Attribute import Attribute
>from classes.Relation import Relation
>from classes.Requests import *
>from classes.DataBase import DataBase


creation de db locale :
>my_db_path = './my_file.sqlite'
>my_db = DataBase(sqlite3.connect(my_db_path))
>my_db_path.fetch_data_from_connection()         
ceci permet de faire une copie de la database dans la mémoire interne du programme

pour des informations sur votre database vous pouvez faire :
>my_db.print_meta()

pour avoir l'access aux relations de votre db, il faut utiliser get_relations() et ensuite selectioner la relation desirée:
>rel_1 = my_db.get_relations()[0]
>rel_2 = my_db.get_relations()[1]
>rel_3 = my_db.get_relations()[2]

vu qu'on a access à tout la database, on peut maintenant écrire et executer des requêtes SPJRUD:

d'abord il faut se decider de quels attributs on a besoin:

>all = Attribute("*","TEXT",0,0,[])  
ceci est le fameux "SELECT * FROM R"

>q0 = Project([all],rel_3)
on doit executer le query pour le transformer en SQL 
>q0.execute()
maintenant on peut l'executer sur la db
>q0.execute_on_db(my_db)


on peut aussi faire des requêtes imbriquées:

>att_salary = Attribute("SALARY","TEXT",0,0,[])
>q1 = Select([att_salary],"=",[20000],company)

ce n'est pas nécessaire d'executer chaque requête car si cette dérnière est utilisée dans une autre requête
elle sera executée automatiquement

>att_salary = Attribute("SALARY","TEXT",0,0,[])
>att_address = Attribute("ADDRESS","TEXT",0,0,[])
>att_name = Attribute("NAME","TEXT",0,0,[])
>q11 = Select([att_name],"=",["Paul"],q1)
>q11.execute(my_db)
>print(q11.sql_query)
>q11.execute_on_db(my_db)