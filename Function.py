# from flask import request
import mysql.connector,datetime
def submitCrawlJob(corp_list):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
    )
    query = "insert into dart.crawl_job values ()"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    inserted_id = mycursor.lastrowid
    #print(inserted_id)
    for bizr_no in corp_list:
        query = f"insert into dart.job_item (biz_no, jobno) values ({bizr_no}, {inserted_id})"
        mycursor.execute(query)
        mydb.commit()
    mydb.commit()
    mycursor.close()
    mydb.close()
    return str(inserted_id)

def registerBizno(corp_list):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
    )
    mycursor = mydb.cursor()
    #print(inserted_id)
    for bizr_no in corp_list:
        query = f"insert into dart.corp_table (bizr_no) values ({bizr_no})"
        mycursor.execute(query)
        mydb.commit()
    mycursor.close()
    mydb.close()
    return

def getjobstatus(jobno):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
    )
    query = f"select status from dart.crawl_job where jobno = {jobno}"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    #print(inserted_id)
    status = mycursor.fetchone()
    mydb.commit()
    mycursor.close()
    mydb.close()
    if (status is None):
        return '-1'
    return str(status[0])