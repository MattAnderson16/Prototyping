import sqlite3

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate in (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The {0} table will be recreated - all existing data will be lost.".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table will be kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()
            
def insert_data(values, db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql = "insert into Customer_Order (Order_ID, Date, Customer_ID) values (?,?,?)"
        cursor.execute(sql,values)
        db.commit()

if __name__ == "__main__":
    db_name = "test.db"
##    sql = """create table Test
##             (TestID integer,
##             Name text,
##             Value real,
##             primary key(TestID))"""
##    create_table(db_name, "Test", sql)
##    values = ("pi",3.14)
##    insert_data(values, db_name)
##    values = ("rnd1", 2.43)
##    insert_data(values, db_name)
##    values = ("rnd2", 5.32)
##    insert_data(values, db_name)
##    values = ("rnd3", 9.21)
##    insert_data(values, db_name)
    sql = """create table Customer_Order
             (Order_ID integer,
             Date text,
             Customer_ID integer,
             primary key(Order_ID))"""
    create_table(db_name, "Customer_Order",sql)
    values = (1,"2014-11-19", 1)
    insert_data(values, db_name)
    values = (2,"2014-11-20", 2)
    insert_data(values, db_name)
    values = (3,"2014-11-21", 3)
    insert_data(values, db_name)    
    values = (4,"2014-11-22", 4)
    insert_data(values, db_name)
    values = (5,"2014-11-20", 5)
    insert_data(values, db_name)
    values = (6,"2014-11-22", 6)
    insert_data(values, db_name)
    values = (7,"2014-11-22", 7)
    insert_data(values, db_name)
    values = (8,"2014-11-22", 8)
    insert_data(values, db_name)
              
##    sql = """create table Order_Items
##             (Order_Item_ID integer,
##             Order_ID integer,
##             Test_ID integer,
##             primary key(Order_Item_ID))"""
##    create_table(db_name, "Order_Items", sql)
##    values = (5,2,5)
##    insert_data(values,db_name)
##    values = (6,3,1)
##    insert_data(values,db_name)
##    values = (7,4,8)
##    insert_data(values,db_name)
##    values = (8,4,7)
##    insert_data(values,db_name)
##    values = (9,4,4)
##    insert_data(values,db_name)
##    values = (10,5,5)
##    insert_data(values,db_name)
##    values = (1,1,1)
##    insert_data(values,db_name)
##    values = (2,1,2)
##    insert_data(values,db_name)
##    values = (3,1,9)
##    insert_data(values,db_name)
##    values = (4,2,3)
##    insert_data(values,db_name)
             
