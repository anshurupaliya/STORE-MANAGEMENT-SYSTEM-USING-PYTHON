import mysql.connector
from email.message import EmailMessage
import re
import smtplib


class Cust:
    def __init__(self): 
        self.mydb = mysql.connector.connect(host="localhost",user="root",password="",database="store")
        self.mycursor = self.mydb.cursor()
        self.cart={}
        self.start() 
        
    def start(self):
            print("")
            print("")
            print("===============================================================")
            print(" ------------ ||||||| LJ BRANDED CLOTH STORE ||||||| ----------")
            print("===============================================================")
            print("")
            print("--> SHIRTS")
            print("--> JACKETS")
            print("--> SHOES")
            print("--> PERFUMES")
            print("")
            print("")
            self.name=str(input("ENTER YOUR NAME = "))
            self.mail=str(input("ENTER YOUR E-MAIL = "))
            while not re.match(r"[^@]+@[^@]+\.[^@]+", self.mail):
                print("INVALID EMAIL FORMAT. PLEASE TRY AGAIN.")
                self.mail = str(input("ENTER YOUR EMAIL: "))
            while True:
                self.phoneno=str(input("ENTER YOUR PHONE_NUMBER = "))
                flag=1
                if(len(self.phoneno)==10):
                    a="123456789"
                    for i in self.phoneno:
                        if not i.isdigit():
                            flag=0
                else:
                    flag=0
                if(flag):
                    print("")
                    self.view()
                    break 
                else:
                    print("***** ENTER VALID PHONE NUMBER ******")
                    
    def view(self):
        while True:
            print("PRESS 1 FOR VIEWING SHIRTS")
            print("PRESS 2 FOR VIEWING JACKETS")
            print("PRESS 3 FOR VIEWING SHOES")
            print("PRESS 4 FOR VIEWING PERFUMES")
            print("PRESS 5 FOR CHECK OUT")
            print("PRESS 6 TO CANCEL ORDER & EXIT")
            print("")
            choice=str(input("ENTER CHOICE = "))
            if choice=="6":
                break
            elif choice=="4":
                self.call("perfumes")
                self.askadd("perfumes")
            elif choice=="1":
                self.call("shirts")
                self.askadd("shirts")
            elif choice=="2":
                self.call("jackets")
                self.askadd("jackets")
            elif choice=="3":
                self.call("shoes")
                self.askadd("shoes")
            elif choice=='5':
                self.bill()
                break
            elif choice=='6':
                break
            else:
                print("******* INVALID CHOICE *******")
                
    def call(self,s):
        query="select * from "+s+";"
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        print("")
        for i in myresult:
            if(i[5]>0):
                print("SR = ", i[0])
                print("CATEGORY_ID = ", i[1])
                print("ITEM_CODE = ", i[2])
                print("NAME = ", i[3])
                print("PRICE = ", i[4])
                print("")

    def askadd(self,s):
        item=str(input("ENTER ITEMCODE YOU WANT TO ADD TO CART = "))
        query="select * from stock;"
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        demo=True
        for i in myresult:
            if i[1]==item.upper():
                self.add(item,s)
                demo=False
                break
        if demo:
            print("ITEM NOT FOUND!!!!")
            print("")
            
    def add(self,itemcode,s):
        query="select * from "+s
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            if i[5]>0 and i[2]==itemcode.upper():
                if itemcode.upper() not in self.cart:
                    query="insert into bill select sr_no,category_id,item_code,name,price from "+s+" where item_code=%s" 
                    adr=(itemcode,)
                    self.mycursor.execute(query,adr)
                    self.mydb.commit()
                    self.cart[itemcode.upper()]=1
                else:
                    self.cart[itemcode.upper()]=self.cart[itemcode.upper()]+1
                print("ITEM ADDED SUCCESSFULLY !!!")
        sql = "update " + s + " set stock =stock-1 where item_code = %s ;"
        adr=(itemcode,)
        self.mycursor.execute(sql,adr)
        self.mydb.commit()
        print("")
        
    def bill(self):
        f=open("bill.txt","w+")
        f.write("\n")
        f.write("===================================================================================\n")
        f.write("----------------------- ||||||| LJ BRANDED CLOTH STORE ||||||| --------------------\n")
        f.write("===================================================================================\n")
        f.write("\n\n\n")
        f.write("NAME = " + self.name.upper() + "\n")
        f.write("CONTACT = " + str(self.phoneno) + "\n")
        f.write("\n\n\n\n")
        f.write("YOUR ITEMS : \n\n")

        query="select * from bill"
        self.mycursor.execute(query)
        myresult = self.mycursor.fetchall()
        price=0
        srno=1
        for i in myresult:
            amount=i[4]*self.cart[i[2].upper()]
            price=price+amount
            
            f.write("SR = " + str(srno) + "\n")
            f.write("CATEGORY_ID = " + i[1] + "\n")
            f.write("ITEM_CODE = " + i[2] + "\n")
            f.write("NAME = " + i[3] + "\n")
            f.write("QUANTITY = " + str(self.cart[i[2]]) + "\n")
            f.write("PRICE = " + str(i[4]) + "\n")
            f.write("AMOUNT = " + str(amount) + "\n")

            f.write("\n\n")
            srno+=1
            
        cgst=9*price/100
        total=price+(2*cgst)
        
        f.write("\n")
        f.write("AMOUNT = " + str(price) + "\n")
        f.write("CGST 9% = " + str(cgst) + "\n")
        f.write("SGST 9% = " + str(cgst) + "\n")
        f.write("\n\n")
        f.write("THE TOTAL AMOUNT TO BE PAID = " + str(price) + " + " + str(cgst) + " + " + str(cgst) + " = " + str(total) + "\n")
        f.write("\n\n\n")
        f.write("-------- ||||||| tHaNk YoU fOr ShOpPiNg ||||||| ---------")

        f.flush()
        f.close()
        
        query="insert into customer_details(name,phone_number,amount) values(%s,%s,%s)" 
        adr=(self.name.upper(),self.phoneno,total)
        self.mycursor.execute(query,adr)
        self.mydb.commit()
        
        sql = "truncate table bill"
        self.mycursor.execute(sql)
        self.mydb.commit()
        
        self.billstorage()
        self.sendmail()
        self.thankyou()
        
    def sendmail(self):
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        f=open("bill.txt","r")
        body=f.read()
        em=EmailMessage()
        em['From']="inventoryshah@gmail.com"
        em['To']=self.mail
        em['Subject']="SUMMARY!"
        em.set_content(str(body))
        server.login("inventoryshah@gmail.com","fwdq qgws fhza shia")
        server.sendmail("inventoryshah@gmail.com",self.mail,em.as_string())
        print("")
        print("YOUR BILL IS SENT TO YOUR RESPECTED E-MAIL")
        
    def billstorage(self):
        f=open("bill.txt","rb")
        data=f.read()
        sql = "insert into bill_storage(name,phone_number,file) values(%s,%s,%s);"
        adr=(self.name.upper(),self.phoneno,data)
        self.mycursor.execute(sql,adr)
        self.mydb.commit()

    
    def thankyou(self):
        print("")
        print("=========================================================")
        print("-------- ||||||| tHaNk YoU fOr ShOpPiNg ||||||| ---------")
        print("=========================================================")

