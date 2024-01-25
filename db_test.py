import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

app = Flask(__name__)

db_name = 'dart'
username = 'root'
password = 'admin'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = '127.0.0.1'
dbname   = '/dart'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and their data type
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

@app.route('/')
def corp_res():
    try:
        a = db.session.query(corpTable.induty_code).filter(corpTable.corp_name.like('%삼성물산%')) # 종목코드 
        query = db.session.query(corpTable.bizr_no,corpTable.stock_name, corpTable.ceo_nm).filter(corpTable.induty_code == a).order_by(corpTable.stock_name)
        corps = query.all()

        corp_text = '<ul>'
        for corp in corps:
            corp_text += '<li>' + corp.bizr_no + ' : ' + corp.stock_name + ' (' + corp.ceo_nm + ')' '</li>'
        corp_text += '</ul>'
        return corp_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
if __name__ == '__main__':
    app.run(debug=True)