# import os
# os.system('pip install --upgrade selenium') selenium 항상 최신버전 유지
import os, time, csv, re, json, sys, pandas,base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import mysql.connector
from selenium.common import exceptions
from selenium.common.exceptions import WebDriverException

# excel_data_df = pandas.read_excel('ETFI112E1.xlsx', sheet_name='Sheet1')
# thisisjson = excel_data_df.to_json(orient='records')
company_name = '대한항공'
json_insertion_sql = "INSERT INTO corp_json (corp_code, corp_content) VALUES (%s, %s)"
excel_insertion_sql = "update dart.corp_table set excel_1 = %s where corp_code = %s"
excel_2_sql = "update dart.corp_table set excel_2 = %s where corp_code = %s"
excel_3_sql = "update dart.corp_table set excel_3 = %s where corp_code = %s"
# same_area_query_sql = "SELECT corp_code, bizr_no, corp_name FROM dart.corp_table where induty_code in (SELECT induty_code FROM dart.corp_table where corp_name like '%" + company_name + "%') limit 30;"
same_area_query_sql = "SELECT corp_code, bizr_no, corp_name FROM dart.corp_table where excel_1 IS NULL limit 100;"


def clearPerformanceLog():
   browser.get_log('performance')

def setExcelResponseBodyToMySQL(company) :
  performance_list = [json.loads(log['message'])['message'] for log in browser.get_log('performance')]
  request_list = []
  response_list = []
  for log in performance_list:
      if log["method"] == "Network.responseReceived" and log["params"]["response"]["url"] =="https://new.cretop.com/solution/excel/download.jsp":
          #requestURL = log["params"]["response"]["headers"]["url"]
          requestId = log["params"]["requestId"]
          try:  
            response = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
            response_list.append(response["body"])
          except exceptions.WebDriverException:           
            print('response.body is null')
          #response = log[response_body]

  print(len(response_list))
  for response_body in response_list:
      print(response_body)     
      val = (response_body , company[0])
      mycursor.execute(excel_insertion_sql, val)
      mydb.commit()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="dart"
)

mycursor = mydb.cursor()
mycursor.execute(same_area_query_sql)
companies = mycursor.fetchall()
print(len(companies))
caps = DesiredCapabilities.CHROME.copy() 
caps['goog:loggingPrefs'] = {"performance": "ALL"}
options = ChromeOptions()

# chrome_options.set_capability("prefs",True)
#options.add_experimental_option('prefs', {'download.defalut_directory':r'C:\Users\rlaal\OneDrive\바탕 화면\Python_Rpa'}) # download 경로지정
#options.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지 옵션
options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
#options.add_argument(r"user-data-dir=C:\\Users\\rlaal\\AppData\\Local\\Google\\Chrome\\User Data")
# name of the directory - change this directory name as per your system

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, desired_capabilities=caps)

# -------------------------------------------------------
url = "https://new.cretop.com"
browser.get(url) # 크레탑으로 이동
wait = WebDriverWait(browser, 10)
time.sleep(4)

for company in companies: 
    print(company[2])  #corp_name
    browser.get("https://new.cretop.com/ET/SS/ETSS070M1") # 크레탑(기업)으로 이동
    time.sleep(4)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > header > div > div.top > div.search-form__area.sub > div.search-form > input[type=text]:nth-child(1)")))
    elem.send_keys(company[1]) # 사업자 등록번호 입력
    time.sleep(4)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='search icon50 icon50 search']")))
    elem.click() # 검색 아이콘 클릭
    time.sleep(4)

    try: # 사업자 번호로 조회 불가 (사업자 번호가 없을)시 예외 처리
      elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > div.container > div > div > div:nth-child(2) > div:nth-child(3) > div.search-result__area > div > ul > li > div > ul.btn__list > li:nth-child(4) > a"))) # 재무 탭
      elem.click() #  검색결과 페이지 로딩완료 및 재무단추 클릭
      time.sleep(4)

      try: # 1. 예외 처리 - 기업이 재무정보 비공개 시 
        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-2']")))
        elem.click()     # 일반기업회계 단추 클릭
        time.sleep(3)

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#forms > option:nth-child(2)")))
        elem.click() # 전계정
        time.sleep(3)

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#etfi110m1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item1 > div > div.inner__area.search-top__area > div > div.btn-wrap > button")))
        elem.click() # 조회하기
        time.sleep(3)

        file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
        if file:
          os.remove(file) # 추가한 파일 삭제
        clearPerformanceLog()

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn excel-download']")))
        # button[class='btn excel-download']
        elem.click() # 엑셀(재무상태표) 다운
        time.sleep(3) # 다운로드 대기
        # Response Body Parsing Case
        # setExcelResponseBodyToMySQL(company)

        fp = open('ETFI112E1.xlsx','rb').read() # 재무상태표 insert
        fp = base64.b64encode(fp)
        args = (fp, company[0])
        mycursor.execute(excel_insertion_sql,args)
        mydb.commit()

        elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "손익계산서")))
        elem.click()
        time.sleep(3)

        file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
        if file:
          os.remove(file) # 추가한 파일 삭제
        clearPerformanceLog()

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#etfi110m1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item2 > div > div > div.table__area > div > div.content__head > div > div > button")))
        elem.click() # 손익계산 다운
        time.sleep(3) # 다운로드 대기

        fp = open('ETFI112E1.xlsx','rb').read() # 손익계산서 insert
        fp = base64.b64encode(fp)
        args = (fp, company[0])
        mycursor.execute(excel_2_sql,args) 
        mydb.commit()

        elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "재무분석")))
        elem.click()
        time.sleep(3)

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-4']")))
        elem.click() # 일반기업회계
        time.sleep(3)

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default w-240 h-56']")))
        elem.click() # 조회하기
        time.sleep(3)

        file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
        if file:
          os.remove(file) # 추가한 파일 삭제
        clearPerformanceLog()

        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#etfi110m1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item4 > div > div:nth-child(3) > div.table__area > div.content__head > div > div > button")))
        browser.execute_script("arguments[0].click()", elem)
        time.sleep(3) # 다운로드 대기

        fp = open('ETFI114E1.xlsx','rb').read() # 재무분석 insert
        fp = base64.b64encode(fp)
        args = (fp, company[0])
        mycursor.execute(excel_3_sql,args) 
        mydb.commit()
      except: # 1. 예외 처리 - 기업이 재무정보 비공개 시 
        try: # 2. 예외 처리 - 로그인 세션 만료 시 
          elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default cancel h-48']"))) # 로그인 하시겠습니까?
          elem.click()
          time.sleep(3)

          elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='close-layer-24 icon24']"))) # 로그인 창 X 
          elem.click()
          time.sleep(3)
          
          elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-login']"))) # 로그인 버튼 
          elem.click()
          time.sleep(3)

          elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default h-48']"))) # 김민성님 로그인 되었습니다 
          elem.click()
        except: 
          elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default h-48']"))) # 재무정보는 고객 요청에따라 공개되지 않습니다.
          elem.click()
          print(company[1]) # 비공개 업체 출력
    except: # 사업자 번호로 조회 불가능한 기업 출력
      print(company[1])