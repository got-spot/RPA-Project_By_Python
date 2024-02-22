import os, time, csv, re, json, sys, pandas, base64
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
from bs4 import BeautifulSoup

excel_insertion_sql = "update dart.corp_table set excel_1 = %s where corp_code = %s"
excel_2_sql = "update dart.corp_table set excel_2 = %s where corp_code = %s"
excel_3_sql = "update dart.corp_table set excel_3 = %s where corp_code = %s"
same_area_query_sql = "SELECT corp_code, bizr_no, corp_name FROM dart.corp_table;"
corp_name_insert_query = "update dart.corp_table set corp_name = %s where bizr_no = %s"

def clearPerformanceLog(browser):
   browser.get_log('performance')

def cretopDown(companies):

  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dart"
  )
  mycursor = mydb.cursor()
  # chrome_options.set_capability("prefs",True)
  caps = DesiredCapabilities.CHROME.copy() 
  caps['goog:loggingPrefs'] = {"performance": "ALL"}
  options = ChromeOptions()
  options.add_argument("--headless=new") # Chrome Headless
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36") 
  options.add_argument("--remote-debugging-port=9222")
  options.add_argument('user-data-dir=C:\\Users\\rlaal\\AppData\\Local\\Google\\Chrome\\User Data')
  options.add_argument("--incognito")
  options.add_argument("--no--sandbox")
  options.add_argument("--disable-setuid-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  # options.add_experimental_option("excludeSwitches", ['enable-logging'])
  options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
  # name of the directory - change this directory name as per your system
  browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, desired_capabilities=caps)

  # -------------------------------------------------------
  url = "https://new.cretop.com"
  browser.get(url) # 크레탑으로 이동
  wait = WebDriverWait(browser, 10)
  time.sleep(3)

  try:
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn txt-blue']"))) # 닫기 버튼
    browser.execute_script("arguments[0].click()", elem)
  except:
    pass

  for company in companies: 
    
    print(company[2])  #corp_name
    browser.get("https://new.cretop.com/ET/SS/ETSS070M1") # 크레탑(기업)으로 이동
    time.sleep(3)

    try:
      elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn btn-login']"))) # 로그인 
      elem.click()
      time.sleep(2)
      elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default h-48']"))) # 확인되었습니다
      elem.click()
      time.sleep(1)
    except:
      pass

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > header > div > div.top > div.search-form__area.sub > div.search-form > input[type=text]")))
    elem.send_keys(company[1]) # 사업자 등록번호 입력
    time.sleep(3)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='search icon50 icon50 search']")))
    elem.click() # 검색 아이콘 클릭
    time.sleep(3)

    try: # 회사이름 insert 시도
      soup = BeautifulSoup(browser.page_source, "html.parser")
      corps = soup.find("button", attrs={"class": "btn result-layer-open"})
      corp = corps.span
      corp_name = corp.get_text()
      args = (corp_name, company[1]) 
      mycursor.execute(corp_name_insert_query, args)
      mydb.commit()
    except:
      print("이미 존재하는 업체입니다.")
    time.sleep(1)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.wrap > div.container > div > div > div:nth-child(2) > div:nth-child(3) > div.search-result__area > div > ul > li > div > ul.btn__list > li:nth-child(4) > a"))) # 재무 탭
    browser.execute_script("arguments[0].click()", elem) #  검색결과 페이지 로딩완료 및 재무단추 클릭
    # a[title='재무 페이지로 이동하기']
    time.sleep(3)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-2']")))
    elem.click()     # 일반기업회계 단추 클릭
    time.sleep(3)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#forms > option:nth-child(2)")))
    elem.click() # 전계정
    time.sleep(3)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default w-240 h-56']")))
    elem.click() # 조회하기
    time.sleep(3)
    browser.execute_script("window.scrollTo(0,100)")

    file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
    if file:
      os.remove(file) # 추가한 파일 삭제
    clearPerformanceLog(browser)
    time.sleep(2)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn excel-download']")))
    # button[class='btn excel-download']
    elem.click() # 엑셀(재무제표) 다운
    time.sleep(3) # 다운로드 대기

    fp = open('ETFI112E1.xlsx','rb').read() # 재무제표 insert
    fp = base64.b64encode(fp)
    args = (fp, company[0])
    mycursor.execute(excel_insertion_sql,args)
    mydb.commit()

    elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "손익계산서")))
    elem.click()
    time.sleep(2)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default w-240 h-56']")))
    elem.click() # 조회하기
    time.sleep(3)

    file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
    if file:
      os.remove(file) # 추가한 파일 삭제
    clearPerformanceLog(browser)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn excel-download']")))
    elem.click() # 손익계산 다운
    time.sleep(3) # 다운로드 대기

    fp = open('ETFI112E1.xlsx','rb').read() # 손익계산서 insert
    fp = base64.b64encode(fp)
    args = (fp, company[0])
    mycursor.execute(excel_2_sql,args) 
    mydb.commit()

    elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "재무분석")))
    elem.click()
    time.sleep(2)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='account-standard-4']")))
    elem.click() # 일반기업회계
    time.sleep(3)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='btn default w-240 h-56']")))
    browser.execute_script("arguments[0].click()", elem) # 조회하기(재무분석)
    time.sleep(3)

    file = next((file for file in os.listdir('.') if re.match('^ETFI', file)), None)
    if file:
      os.remove(file) # 추가한 파일 삭제
    clearPerformanceLog(browser)

    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#etfi110m1 > div > div:nth-child(3) > div > div > div > div.tab-item.teb-item4 > div > div:nth-child(3) > div.table__area > div.content__head > div > div > button"))) # 재무분석 (엑셀버튼 클릭 실패로 상기 코드(selector)로 수정)
    # elem.click()
    browser.execute_script("arguments[0].click()", elem) # 다운로드 클릭
    time.sleep(3) # 다운로드 대기

    try:
      fp = open('ETFI114E1.xlsx','rb').read() # 재무분석 insert
      fp = base64.b64encode(fp)
      args = (fp, company[0])
      mycursor.execute(excel_3_sql,args) 
      mydb.commit()
    except:
      pass