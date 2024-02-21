import pymysql
from flask import Flask, request, render_template, Response
import mysql.connector
# from getExcelStreamByCompanyName import getExcelStreamByCompanyName
from Function import submitCrawlJob,getjobstatus, registerBizno
from make_excel import getExcelStreamByCompanyName, getExcelStreamByJobno

app = Flask(__name__)

@app.route('/') # 홈페이지
def index(): # home
    return form()

def form():
    content = '''
       <form action="/corp/companies" method = 'POST'>
            <input type="text" name="corp" placeholder="기업 이름 입력">
            <input type="submit" value="검색">
        </form>
    '''
    return content
    
@app.route('/corp/companies', methods = ['POST', 'GET'])
def corp_res():
    if request.method == 'POST':
        global corp 
        corp = request.form["corp"]
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="dart"
        )
        query = f"select * FROM dart.corp_table where induty_code in (select induty_code from dart.corp_table where stock_name like '%{corp}%');"
        mycursor = mydb.cursor()
        mycursor.execute(query)
        corps = mycursor.fetchall()
        return render_template('result.html', corps=corps)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text 

@app.route('/downloadExcel', methods = ['POST', 'GET']) # URL 설정하기
def CretopDown():

    ''' 목록을 URL로 받았을 때
    corp_list = request.form.getlist('check')
    corp_text = '('
    i = 0
    for bizr_no in corp_list:
        corp_text += "'" + bizr_no + "'"
        i += 1
        if i < len(corp_list):
            corp_text += ","
    corp_text += ')'

    output = getExcelStreamByCompanyName(corp_text)
    '''
    # jobno만 받고 회사목록은 DB에서 Select 할 때
    output = getExcelStreamByJobno(request.values['jobno'])
    # return output
    response = Response(
        output.getvalue(),
        mimetype="application/vnd.ms-excel",
        content_type='application/octet-stream',
    )
    response.headers["Content-Disposition"] = "attachment; filename=merged.xlsx" # 다운받았을때의 파일 이름 지정해주기
    return response

@app.route('/crawlRequest', methods = ['POST', 'GET']) # URL 설정하기
def crawlRequest():
    selected_corp_list = request.form.getlist('selectedCompany')
    added_corp_list = request.form.getlist('addedCompany')
    registerBizno(added_corp_list)
    corp_list = selected_corp_list + added_corp_list
    output = submitCrawlJob(corp_list)
    return render_template('ajax.html',output=output)

@app.route('/AjaxCrawlStatus', methods = ['POST', 'GET']) # URL 설정하기
def AjaxCrawlStatus():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
    )
    mycursor = mydb.cursor()
    #jobno = mycursor.lastrowid
    jobno = request.values['jobno']
    if (jobno == None):
        return '-1'
    output = getjobstatus(jobno)
    return output

@app.route('/CrawlStatus', methods = ['POST', 'GET']) # URL 설정하기
def CrawlStatus():
    jobno = request.values['jobno']
    return render_template('ajax.html',output=jobno)

@app.route('/biznoValidate', methods = ['POST', 'GET']) # URL 설정하기
def biznoValidate():
    bizno = request.values['bizno']
    return render_template('ajax.html',output=bizno)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)