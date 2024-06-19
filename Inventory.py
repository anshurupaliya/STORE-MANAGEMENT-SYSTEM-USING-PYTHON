import mysql.connector

class Invent:
    def __init__(self): 
        self.mydb = mysql.connector.connect(host="localhost",user="root",password="",database="store")
        self.mycursor = self.mydb.cursor()
        self.verify()
        self.start()
        
    def verify(self):
        while True:
            print("")
            user=str(input("ENTER USERNAME = "))
            password=str(input("ENTER PASSWORD ="))
            print("")
            if(user=="admin" and password=="admin"):
                break
            else:
                print("******* INVALID CREDENTIALS *******")
        
    def start(self):
        while True:
            print("PRESS 1 TO SEE STOCK")
            print("PRESS 1 TO ADD STOCK")
            print("PRESS 3 TO EXIT")
            choice=str(int(input("CHOICE = ")))
            print("")
            if(choice=="1"):
                self.view()
            elif choice=="2":
                self.add()
            elif choice=="3":
                break
            else:
                print("******* INVALID CHOICE *******")
    
    def view(self):
        while True:
            print("PRESS 1 FOR SHIRT STOCK")
            print("PRESS 2 FOR JACKETS STOCK")
            print("PRESS 3 FOR SHOES STOCK")
            print("PRESS 4 FOR PERFUMES STOCK")
            print("PRESS 5 TO GO BACK")
            print("PRESS 6 TO EXIT")
            choice=str(int(input("CHOICE = ")))
            print("")
            if choice=="6":
                break
            elif choice=="1":
                self.stock("shirts")
            elif choice=="2":
                self.stock("jackets")   
            elif choice=="3":
                self.stock("shoes")
            elif choice=="4":
                self.stock("perfumes")
            elif choice=="5":
                self.start()
            else:
                print("******* INVALID CHOICE *******")
                
    def stock(self,table):
        query="select * from "+table
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            print("SR = ", i[0])
            print("ITEM_CODE = ", i[2])
            print("NAME = ", i[3])
            print("STOCK = ",i[5])
            print("")
    
    def add(self):
        item_code=str(input("ENTER ITEM CODE WHOSE STOCK YOU WANT TO ADD = "))
        flag=False
        query="select * from stock;"
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            if i[1].upper()==item_code.upper():
                flag=True
        if flag:
            choice=item_code[1]
            table=""
            if choice=="1":
                table="shirts"
            elif choice=="2":
                table="jackets"   
            elif choice=="3":
                table="shoes"
            elif choice=="4":
                table="perfumes"
            
            quantity=int(input("ENTER QUANTITY = "))
            print("")
            sql = "update " + table + " set stock =stock+%s where item_code = %s ;"
            adr=(quantity,item_code.upper())
            self.mycursor.execute(sql,adr)
            self.mydb.commit()
            print("--- === STOCK UPDATED SUCCESSFULLY  === ---")
            print("")
        else:
            print("--- === ENTERED ITEMCODE DOES NOT EXIST  === ---")
            print("")
                