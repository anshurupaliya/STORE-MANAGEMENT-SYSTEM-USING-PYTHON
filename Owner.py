import mysql.connector;


class Owner:
    def __init__(self): 
        self.mydb = mysql.connector.connect(host="localhost",user="root",password="",database="store")
        self.mycursor = self.mydb.cursor()
        self.own()
        self.next()
    
    def own(self):
        while True:
            print("")
            user=str(input("ENTER USERNAME = "))
            password=str(input("ENTER PASSWORD ="))
            print("")
            if(user=="admin" and password=="admin"):
                break
            else:
                print("******* INVALID CREDENTIALS *******")
    
    def next(self):
        while True:
            print("PRESS 1 FOR MANIPULATING SHIRT")
            print("PRESS 2 FOR MANIPULATING JACKETS")
            print("PRESS 3 FOR MANIPULATING SHOES")
            print("PRESS 4 FOR MANIPULATING PERFUMES")
            print("PRESS 5 FOR EXTRACTING BILLS")
            print("PRESS 6 FOR GEETING CUSTOMER DETAILS")
            print("PRESS 7 FOR EXIT")
            print("")
            choice=str(input("ENTER CHOICE = "))
            if choice=="7":
                break
            elif choice=="1":
                self.updatechoice("shirts")
                choice1=str(input("DO YOU WANT TO CONTINUE(Y=1/N) ="))
                if choice!="1":
                    break
            elif choice=="2":
                self.updatechoice("jackets")
                choice1=str(input("DO YOU WANT TO CONTINUE(Y=1/N) ="))
                if choice!="1":
                    break
            elif choice=="3":
                self.updatechoice("shoes")
                choice1=str(input("DO YOU WANT TO CONTINUE(Y=1/N) ="))
                if choice!="1":
                    break
            elif choice=="4":
                self.updatechoice("perfumes")
                choice1=str(input("DO YOU WANT TO CONTINUE(Y=1/N) ="))
                if choice!="1":
                    break
            elif choice=="5":
                self.extractbill()
            elif choice=="6":
                self.getcustomer()
            else:
                print("******* INVALID CHOICE *******")
                
    def updatechoice(self,tablename):
        print("PRESS 1 FOR DELETING ENTRY")
        print("PRESS 2 FOR UPDATING PRICE")
        print("PRESS 3 FOR INSERTING ENTRY")
        print("PRESS 4 TO RETURN")
        print("PRESS 5 TO EXIT")
        print("")
        while True:
            choice=str(input("ENTER YOUR CHOICE = "))
            if choice=="5":
                break
            elif choice=="4":
                self.next()
                break
            elif choice=="1":
                self.delete(tablename)
                break
            elif choice=="2":
                self.update(tablename)
                break
            elif choice=="3":
                self.insert(tablename)
                break
            else:
                print("******* INVALID CHOICE *******")
                    
    def delete(self,tablename):
        item=str(input("ENTER ITEMCODE WHOSE DATA YOU WANT TO DELETE = ")).upper()
        sql = "delete from " + tablename + " where ITEM_CODE = %s ;"
        adr=(item)
        self.mycursor.execute(sql,adr)
        self.mydb.commit()
        if self.mycursor.rowcount>0:
            print("--- === UPDATED SUCCESSFULLY === ---")
        else:
            print("--- === ENTERED ITEMCODE DOES NOT EXIST  === ---")
                
    def update(self,tablename):
        item=str(input("ENTER ITEMCODE WHOSE DATA YOU WANT TO UPDATE = ")).upper()
        price=int(input("ENTER PRICE = "))
        sql = "update " + tablename + " set PRICE = %s where item_code = %s ;"
        adr=(price,item)
        self.mycursor.execute(sql,adr)
        self.mydb.commit()
        if self.mycursor.rowcount>0:
            print("--- === UPDATED SUCCESSFULLY === ---")
        else:
            print("--- === ENTERED ITEMCODE DOES NOT EXIST  === ---")
                
    def insert(self,tablename):
        categoryid=str(input("ENTER CATEGORY_ID = ")).upper()
        item=str(input("ENTER ITEMCODE = ")).upper()
        name=str(input("ENTER NAME = "))
        price=int(input("ENTER PRICE = "))
        
        sql = "insert into " + tablename + " (CATEGORY_ID,ITEM_CODE,NAME,PRICE) values(%s,%s,%s,%s) ;"
        adr=(categoryid,item,name,price)
        self.mycursor.execute(sql,adr)
        self.mydb.commit()
        if self.mycursor.rowcount>0:
            print("--- === UPDATED SUCCESSFULLY === ---")
        else:
            print("--- === ENTERED ITEMCODE DOES NOT EXIST  === ---")
                
    def extractbill(self):
        sql = "select * from bill_storage;"
        self.mycursor.execute(sql)
        #self.mydb.commit()
        myresult = self.mycursor.fetchall()
        name=str(input("ENTER NAME WHOSE BILL YOU WANT = "))
        for i in myresult:
            if i[1].upper()==name.upper():
                f1="D:\\PYTHON PROJECT\\BILLS\\" + name + ".txt"
                with open(f1, 'wb') as fi:
                    fi.write(i[3])
            
    def getcustomer(self):
        sql = "select * from customer_details details order by amount desc"
        self.mycursor.execute(sql)
        #self.mydb.commit()
        myresult = self.mycursor.fetchall()
        print("THE DETAILS OF CUSTOMERS ARE AS FOLLOWS")
        print("")
        for i in myresult:
            print(i[1].upper() + "     ",end="")
            print(i[2],end="   ")
            print(i[3])
        print("")