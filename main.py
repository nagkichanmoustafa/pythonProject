from tkinter import *
import sqlite3
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import sys


cap = cv2.VideoCapture(cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)


def click_evnt(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        card()

def card():
    root2 = Tk()
    root2.title("Basket")
    root2.geometry("600x500")

    def basket_list():
        con2 = sqlite3.connect("basket.db")
        curser2 = con2.cursor()

        curser2.execute("SELECT * FROM basket")
        rcr = curser2.fetchall()
        print(rcr)
        print_rcr = ''

        for record in rcr:
            print_rcr += str(record[0]) + " ...........  " + str(record[1]) + " tl\n"

        basket_label = Label(root2)
        basket_label.config(text=print_rcr, font=("Arial", 9))
        basket_label.place(x=45, y=90)

        con2.commit()
        con2.close()

    def total():
        con2 = sqlite3.connect("basket.db")
        curser2 = con2.cursor()

        topl = curser2.execute("SELECT SUM(product_price) FROM basket")
        topl = curser2.fetchall()

        total_label = Label(root2)
        price_label = Label(root2)
        price_label.config(text="tl", font=("Arial", 9))
        price_label.place(x=220, y=90)
        total_label.config(text=topl, font=("Arial", 9))
        total_label.place(x=190, y=90)

    def cl():
        con2 = sqlite3.connect("basket.db")
        curser2 = con2.cursor()
        curser2.execute("DELETE FROM basket")
        root2.destroy()
        con2.commit()
        con2.close()
        sys.exit()

    def delete():
        con2 = sqlite3.connect("basket.db")
        curser2 = con2.cursor()
        curser2.execute("DELETE FROM basket WHERE product_name=?", (product_name.get(),))
        con2.commit()
        con2.close()
        product_name.delete(0, END)

    basket_btn = Button(root2, text="List", command=basket_list)
    basket_btn.place(x=50, y=50)
    tpl_btn = Button(root2, text="Total", command=total)
    tpl_btn.place(x=180, y=50)

    kpt_btn = Button(root2, text="Exit", command=cl)
    kpt_btn.place(x=10, y=10)

    pay_btn = Button(root2, text="Confirm Payment", command=pay)
    pay_btn.place(x=450, y=10)

    product_name = Entry(root2)
    product_name.place(x=360, y=50)

    product_name_label = Label(root2)
    product_name_label.config(text="Product name : ", font=("Arial", 9))
    product_name_label.place(x=260, y=50)
    delete_btn = Button(root2, text="Delete", command=delete)
    delete_btn.place(x=500, y=50)

    root2.mainloop()

con2 = sqlite3.connect("basket.db")
curser2 = con2.cursor()

def pay():
    root3 = Tk()
    root3.title("pay")
    root3.geometry("500x200")

    def ext():
        con2 = sqlite3.connect("basket.db")
        curser2 = con2.cursor()
        curser2.execute("DELETE FROM basket")
        root3.destroy()
        con2.commit()
        con2.close()
        sys.exit()


    name_label = Label(root3)
    name_label.config(text="You can make the payment!", font=("Arial", 15))
    name_label.place(x=20, y=70)
    exit_btn = Button(root3, text="Exit" ,command = ext)
    exit_btn.place(x=10, y=10)


    root3.mainloop()




def basket():
    con2 = sqlite3.connect("basket.db")
    curser2 = con2.cursor()
    curser2.execute("CREATE TABLE IF NOT EXISTS basket (product_name TEXT,product_price INT,product_code TEXT )")
    con2.commit()
basket()

curser2.execute("SELECT product_code FROM basket")
myDataList2=(curser2.fetchall())


con = sqlite3.connect("product_list.db")
curser = con.cursor()


def list1():

    curser.execute("CREATE TABLE IF NOT EXISTS product_list (product_name TEXT, product_price INT,product_code TEXT )")
    con.commit()

list1()
curser.execute("SELECT product_code FROM product_list")
myDataList = (curser.fetchall())

print(myDataList)


while True:
    success, img = cap.read()
    con = sqlite3.connect("product_list.db")
    curser = con.cursor()

    curser.execute("SELECT * FROM product_list")
    recordss=curser.fetchall()


    for barcode in decode(img):

        myData = barcode.data.decode('utf-8')
        print(myData)

        if myData in str(myDataList):
            con2 = sqlite3.connect("basket.db")
            curser2 = con2.cursor()
            con = sqlite3.connect("product_list.db")
            curser = con.cursor()
            curser.execute("SELECT product_name,product_price FROM product_list WHERE product_code=?",(myData,))
            record = curser.fetchone()
            myOutput=record
            myColor=(0,255,0)
            counter = 0
            if myData not in str(myDataList2):
                curser2.execute("INSERT INTO basket VALUES (:product_name, :product_price, :product_code) ",
                            {

                                'product_name': record[0],
                                'product_price': record[1],
                                'product_code': myData,

                            })

                con2.commit()
                con2.close()
                myDataList2.append(myData)


            else:
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, myColor, 5)
                pts2 = barcode.rect
                cv2.putText(img, str(myOutput), (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

            con.commit()
            con.close()

        else:

            myOutput = ' '
            myColor = (0, 0, 255)
            root = Tk()
            root.title("addProduct")

            con = sqlite3.connect("product_list.db")
            curser = con.cursor()

            def submit():

                con = sqlite3.connect("product_list.db")
                curser = con.cursor()
                curser.execute("INSERT INTO product_list VALUES (:product_name, :product_price, :product_code) ",
                               {

                                   'product_name': product_name.get(),
                                   'product_price': product_price.get(),
                                   'product_code': myData,

                               })

                con.commit()
                con.close()

                product_name.delete(0, END)
                product_price.delete(0, END)

            def query():
                con = sqlite3.connect("product_list.db")
                curser = con.cursor()


                curser.execute("SELECT * FROM product_list")
                records = curser.fetchall()
                print(records)
                print_records = '\n'

                for record in records:
                    print_records += str(record[0]) + "   " + str(record[1]) + "   " + str(record[2]) + "\n"
                query_label = Label(root)
                query_label.config(text=print_records, font=("Arial", 9))
                query_label.place(x=100, y=300)



            def clsd():
                root.destroy()



            def delete():

                con = sqlite3.connect("product_list.db")
                curser = con.cursor()
                curser.execute("DELETE FROM product_list WHERE product_name=?", (product_name.get(),))
                con.commit()
                con.close()

                product_name.delete(0, END)


            product_name = Entry(root)
            product_name.place(x=150, y=70)

            product_price = Entry(root)
            product_price.place(x=150, y=90)

            product_name_label = Label(root)
            product_name_label.config(text="Enter Product Name *", font=("Arial", 9))
            product_name_label.place(x=20, y=70)

            product_price_label = Label(root)
            product_price_label.config(text="Enter Product Price *", font=("Arial", 9))
            product_price_label.place(x=20, y=90)

            submit_btn = Button(root, text="Save", command=submit)
            submit_btn.place(x=270, y=150)



            query_btn = Button(root, text="Show All Products ", command=query)
            query_btn.place(x=200, y=200)

            clsd_btn = Button(root, text="Exit", command=clsd)
            clsd_btn.place(x=10, y=20)

            card_btn = Button(root, text="Basket" , command = card)
            card_btn.place(x=250, y=20)

            delete_btn = Button(root, text="Delete by Name", command=delete)
            delete_btn.place(x=50, y=200)


            con.commit()
            con.close()
            root.geometry("500x600")
            root.mainloop()
            myDataList.append(myData)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, str(myOutput), (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.setMouseCallback('Result', click_evnt)
    cv2.waitKey(1)