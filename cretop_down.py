# import os
# os.system('pip install --upgrade selenium') selenium 항상 최신버전 유지
import os, time, csv, re, json, sys, pandas
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

select_sql = 'SELECT bizr_no FROM dart.corp_table limit 3000;' 

# company_name = '대한항공'
json_insertion_sql = "INSERT INTO corp_json (corp_code, corp_content) VALUES (%s, %s)"
excel_insertion_sql = "INSERT INTO corp_table (corp_code, excel_1) VALUES (%s, %s)"
# same_area_query_sql = "SELECT corp_code, bizr_no, corp_name FROM dart.corp_detail where induty_code in (SELECT induty_code FROM dart.corp_detail where corp_name like '%" + company_name + "%') limit 30;"
same_area_query_sql = "SELECT corp_code, bizr_no, corp_name FROM dart.corp_table where induty_code = 26410;"

def clearPerformanceLog():
   browser.get_log('performance')

def setResponseBodyToMySQL(company) :
  performance_list = [json.loads(log['message'])['message'] for log in browser.get_log('performance')]
  request_list = []
  response_list = []
  for log in performance_list:
      if log["method"] == "Network.responseReceived" and log["params"]["response"]["url"] =="https://new.cretop.com/httpService/request.json":
          #requestURL = log["params"]["response"]["headers"]["url"]
          requestId = log["params"]["requestId"]
          try:  
            response = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})

            #request_list.append(log)
            response_json = json.loads(response["body"])
            #print(response_json["header"]["screenId"])
            if (response_json["header"]["screenId"][0:7] == "ETFI112" or response_json["header"]["screenId"][0:7] == "ETFI114" ):             
                response_list.append(response_json)
          except exceptions.WebDriverException:           
            print('response.body is null')
          #response = log[respons"e_body]

  print(len(response_list))
  for response_body in response_list:
      #print(response_body)
      
      val = (company[0], json.dumps(response_body))
      mycursor.execute(json_insertion_sql, val)
      mydb.commit()


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
      #print(response_body)     
      val = (company[0], response_body)
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
time.sleep(2)


'''
for company in companies:
    print(company[2])
    browser.get("https://new.cretop.com/ET/SS/ETSS070M1") # 크레탑(기업)으로 이동
    browser.set_window_size(1920, 1080)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > header > div > div.top > div.search-form__area.sub > div.search-form > input[type=text]:nth-child(1)")))
    elem.send_keys(company[1]) # 사업자 등록번호 입력

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > header > div > div.top > div.search-form__area.sub > div.search-form > button")))
    elem.click() #  검색결과 페이지 로딩완료 및 재무단추 클릭 

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label ")))
    elem.click()     # 일반기업회계 단추 클릭

    clearPerformanceLog()
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-2']" )))
    elem.click()
    setResponseBodyToMySQL(company) 

    clearPerformanceLog()
    elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "손익계산서")))
    elem.click()
    time.sleep(1) 
    setResponseBodyToMySQL(company)

    elem =  wait.until(EC.presence_of_element_located((By.LINK_TEXT, "재무분석")))
    elem.click()

    clearPerformanceLog()
    elem =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for = 'account-standard-4']")))
    elem.click()
    time.sleep(1) 
    setResponseBodyToMySQL(company)
'''


for company in companies: 
  print(company[2])
  browser.get("https://new.cretop.com/ET/SS/ETSS070M1") # 크레탑(기업)으로 이동
  browser.set_window_size(1920, 1080)

  elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > header > div > div.top > div.search-form__area.sub > div.search-form > input[type=text]:nth-child(1)")))
  elem.send_keys(company[1]) # 사업자 등록번호 입력

  elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='search icon50 icon50 search']")))
  elem.click() # 검색 엔터

  try:
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > div.container > div > div > div:nth-child(2) > div:nth-child(3) > div.search-result__area > div > ul > li > div > ul.btn__list > li:nth-child(4) > a")))
    elem.click() #  검색결과 페이지 로딩완료 및 재무단추 클릭 

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-2']")))
    elem.click()     # 일반기업회계 단추 클릭

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#forms > option:nth-child(2)")))
    elem.click() # 전계정

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#etfi110m1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item1 > div > div.inner__area.search-top__area > div > div.btn-wrap > button")))
    elem.click() # 조회하기
    browser.execute_script("window.scrollTo(0, 100)")

    time.sleep(1)
    clearPerformanceLog()

    browser.find_element(By.CSS_SELECTOR, "button[class='btn excel-download']").click() # 엑셀(재무상태표) 다운

    time.sleep(1.5) # 다운로드 대기
  # setExcelResponseBodyToMySQL(company)
  except:
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default h-48']")))
    elem.click()
  #insert_sql = 'INSERT INTO corp_table (excel_1) VALUES (' + filename + ');'

  #mycursor = mydb.cursor()
  #mycursor.execute(insert_sql)
  #mydb.commit()