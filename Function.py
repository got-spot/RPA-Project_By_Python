
# from flask import request
import mysql.connector,datetime
def submitCrawlJob(corp_list):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
    )
    now = datetime.datetime.now()
    query = f"insert into dart.crawl_job values (null, 0, now()); SELECT LAST_INSERT_ID();"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    data = mycursor.fetchall()
    #mycursor.close()
    print(data)
    inserted_id = data
    for bizr_no in corp_list:
        query = f"insert into dart.job_item values (null, {bizr_no}, {inserted_id})"
        mycursor.execute(query)
    return data[0]


  