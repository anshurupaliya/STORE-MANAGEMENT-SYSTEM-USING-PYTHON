import mysql.connector
import Owner as o
import Customer as c
import Inventory as i

mydb = mysql.connector.connect(host="localhost",user="root",password="",database="store")
mycursor = mydb.cursor()


sql = "truncate table bill"
mycursor.execute(sql)
mydb.commit()



print("")
print("")
print("PRESS 1 FOR OWNER")
print("PRESS 2 FOR CUSTOMER")
print("PRESS 3 FOR INVENTORY MANAGEMENT")
print("PRESS ANY OTHER KEY TO EXIT")
choice=str(input("ENTER YOUR CHOICE = "))

if(choice=="1"):
    o1=o.Owner()
elif(choice=="2"):
    c1=c.Cust()
elif(choice=="3"):
    i1=i.Invent()