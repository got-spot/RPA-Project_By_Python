import io
import zipfile
import requests
from xml.etree.ElementTree import parse
import pandas as pd
import time
import datetime

crtfc_key='a6bc7e55fd8b7651c17ced55076762f2099e00cc'

#회사정보 가져오기
#임의로 'E:/' 로 설정 및 다운로드 파일 corpcode.zip으로 설정
path='C:\\Users\\김민준\\Desktop\\Rpa\\'
filename='corpcode.zip'

url = 'https://opendart.fss.or.kr/api/corpCode.xml'
params = {
    'crtfc_key': crtfc_key,
}
results=requests.get(url, params=params)

file = open(path+filename, 'wb')
file.write(results.content)
file.close()

zipfile.ZipFile(path+filename).extractall(path)

tree = parse(path + 'CORPCODE.xml')
root = tree.getroot()
li=root.findall('list')
corp_code,corp_name,stock_code,modify_date=[],[],[],[]
for d in li:
    corp_code.append(d.find('corp_code').text)
    corp_name.append(d.find('corp_name').text)
    stock_code.append(d.find('stock_code').text)
    modify_date.append(d.find('modify_date').text)
corps_df = pd.DataFrame({'corp_code':corp_code,'corp_name':corp_name,
         'stock_code':stock_code,'modify_date':modify_date})

corps_df = corps_df.loc[corps_df['stock_code']!=' ',:].reset_index(drop=True)

#전체결과저장
result_all=[]
corf_detail=pd.DataFrame()

print('총 회사수는 : ' + str(corps_df.shape[0]))

# 수집한 회사에 대해서 for문.
for i, r in corps_df.iterrows():
    #if i == 2:
    #    break
    
    #없으면 어느 시점에서 에러발생
    time.sleep(0.1)
    
    print('i = ' + str(i))
    corp_code=str(r['corp_code'])
    corp_name=r['corp_name']

    url = 'https://opendart.fss.or.kr/api/company.json'
    params = {
        'crtfc_key': crtfc_key,
        'corp_code' : corp_code,
    }

    results = requests.get(url, params=params).json()
    # 응답이 정상 '000' 일 경우에만 데이터 수집
    if results['status'] == '000':
        result_all.append(results)    

corp_detail=pd.DataFrame(result_all)

# corps_df = corps_df.loc[corps_df['stock_code']!=' ',:].reset_index(drop=True)
corp_detail = corp_detail.loc[corp_detail['corp_cls']=="N"].reset_index(drop=True)
corp_detail = corp_detail.loc[corp_detail['corp_cls']=="E"].reset_index(drop=True)

print('총 유가/코스닥 회사수는 : ' + str(corp_detail.shape[0]))
# corp_detail.to_csv('e:/회사상세정보.csv') 이게 아니라
# corp_detail.to_sql <- 이걸로 DB에 저장