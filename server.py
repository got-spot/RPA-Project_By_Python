import pymysql
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import mysql.connector
# from getExcelStreamByCompanyName import getExcelStreamByCompanyName
from Function import submitCrawlJob,getjobstatus, registerBizno
from make_excel import getExcelStreamByCompanyName, getExcelStreamByJobno

db = SQLAlchemy()
app = Flask(__name__)

# MySQL 연결 설정
db_name = 'dart'
username = 'root'
password = 'admin'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/dart'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

class corpTable(db.Model):
    __tablename__ = 'corp_table'
    status = db.Column(db.Text)
    message = db.Column(db.Text)
    corp_code = db.Column(db.Text)
    corp_name = db.Column(db.Text)
    corp_name_eng = db.Column(db.Text)
    stock_name = db.Column(db.Text)
    stock_code = db.Column(db.Text)
    ceo_nm = db.Column(db.Text)
    corp_cls = db.Column(db.Text)
    jurir_no = db.Column(db.Text)
    bizr_no = db.Column(db.Text, primary_key=True)
    adres = db.Column(db.Text)
    hm_url = db.Column(db.Text)
    ir_url = db.Column(db.Text)
    phn_no = db.Column(db.Text)
    fax_no = db.Column(db.Text)
    induty_code = db.Column(db.Text)
    est_dt = db.Column(db.Text)
    acc_mt = db.Column(db.Text)

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


# @app.route('/corp/companies', methods = ['POST', 'GET'])
# def corp_res():
#     if request.method == 'POST':
#         global corp 
#         corp = request.form["corp"]
#     try:
#         subquery = db.session.query(corpTable.induty_code).filter(corpTable.corp_name.like(f'%{corp}%')).scalar_subquery() # 종목코드 
#         query = db.session.query(corpTable.bizr_no,corpTable.stock_name, corpTable.ceo_nm).filter(corpTable.induty_code == subquery) # .order_by(corpTable.stock_name)
#         corps = query.all()
#         return render_template('result.html', corps=corps)
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text 
    
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
    # return output
    # print(output)
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


# @app.route('/download', methods = ['POST', 'GET']) # URL 설정하기
# def download():
#     # CSV 파일 형태로 브라우저가 파일다운로드라고 인식하도록 만들어주기
#     if request.method == 'POST':
#         corp = request.form["corp"]
#     output = getExcelStreamByCompanyName('대한항공')
#     response = Response(
#         output.getvalue(),
#         mimetype="application/vnd.ms-excel",
#         content_type='application/octet-stream',
#     )
#     response.headers["Content-Disposition"] = "attachment; filename=merged.xlsx" # 다운받았을때의 파일 이름 지정해주기
#     return response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)