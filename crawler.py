import mysql.connector, time
from cretopDown import cretopDown

def updateStatus(jobno):
    query = "update dart.crawl_job set status = 1 where jobno = %s"
    mycursor = mydb.cursor()
    param = (jobno,)
    mycursor.execute(query, param)
    mydb.commit()
    mycursor.close()
    return 

def getCrawlTarget():
    query = "select jobno from dart.crawl_job where status = 0 order by jobno asc limit 1"
    query2 = "select b.corp_code, a.biz_no, b.corp_name from dart.job_item a, dart.corp_table b where a.biz_no = b.bizr_no and excel_3 is null and jobno = %s;"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    jobno  = mycursor.fetchall()
    print(jobno)
    param = (jobno[0][0],)
    mycursor.execute(query2, param)
    data = mycursor.fetchall()
    mycursor.close()
    return jobno, data

def checkQueue():
    query = "select count(*) from dart.crawl_job where status = 0"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    data  = mycursor.fetchall()
    isJobwaiting = data[0][0]
    mydb.commit()
    mycursor.close()
    #print (isJobwaiting)
    if isJobwaiting > 0:
        return True
    else:
        return False

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="admin",
database="dart"
)


while True:
    if checkQueue():
        jobno, companies = getCrawlTarget()
        print("getCrawlTarget : number of crawling targets = " + str(len(companies)) + " of jobno " + str(jobno[0][0]))
        cretopDown(companies)
        #print ("in check Queue")
        #print (jobno[0][0])
        # time.sleep(30)
        updateStatus(jobno[0][0])
        print ("Loop: jobno " + str(jobno[0][0]) + " is completed.")
