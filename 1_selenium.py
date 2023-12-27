import os, time
# os.system('pip install --upgrade selenium') selenium 항상 최신버전 유지
# pip install lxml

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지 옵션
options.add_experimental_option('prefs', {'download.defalut_directory':r'C:\Users\rlaal\OneDrive\바탕 화면\Python_Rpa'}) # download 경로지정
browser = webdriver.Chrome(options=options)

browser.get("https://new.cretop.com/?h=1702989839177") # 크레탑으로 이동
time.sleep(2)

browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/button').click() #닫기 버튼 
browser.find_element(By.ID, "idModel").send_keys("KAC100") # ID 입력
browser.find_element(By.ID, "pwModel").send_keys("kac100!!") # PW 입력
browser.find_element(By.CSS_SELECTOR, "[title='로그인']").click() # 로그인 

time.sleep(1)
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/button[2]').click() # 본인인증 

time.sleep(1)
browser.find_element(By.LINK_TEXT, "휴대폰 인증").click() 

browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/ul/li[3]/span/label').click() #통신사 선택 # li[1] : SK li[2] : KT li[3] : LG
browser.find_element(By.ID, "PLCM050P1_agency-check-all").click() # 약관 전체동의
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/button').click() # 다음 버튼
browser.find_element(By.NAME, "PLCM050P2_username").send_keys("김민성")
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div[2]/div/span[1]/label').click() #내국인
browser.find_element(By.ID, 'PLCM050P2_birth').send_keys("20010426")
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/span[1]/label').click() # 성별(남자)선택
browser.find_element(By.ID, "PLCM050P2_phone2").send_keys("4373")
browser.find_element(By.ID, "PLCM050P2_phone3").send_keys("6549")
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/button').click() #인증번호 요청
time.sleep(1)
browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/ul/button').click() #인증번호가 전송되었습니다 [확인] 버튼클릭

# browser.find_element(By.ID, "PLCM050P2_certifyNumber").send_keys("인증번호6자리")
# -----------------------수동입력-----------------------------------------------------

time.sleep(30) #문자 입력 대기


browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div/button').click() #인증 버튼
time.sleep(1)

browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div/div/ul/button').click() # 본인인증이 성공하였습니다 [확인] 버튼
time.sleep(1)

browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div/div/ul/button').click() # 다시 로그인 해주세요 [확인] 버튼
time.sleep(1)

browser.find_element(By.ID, "pwModel").send_keys("kac100!!") # PW 입력
browser.find_element(By.CSS_SELECTOR, "[title='로그인']").click() #로그인 클릭
time.sleep(2)

browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div/div/ul/button').click() # 김민성님 로그인 되었습니다 [확인] 버튼
time.sleep(5)

browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/input[1]').send_keys("삼성물산") # 검색어 입력

browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/button').click() # 검색버튼 클릭.

browser.find_element(By.XPATH, '//*[@id="et-area"]/div/div[2]/ul/li[1]/div/ul[3]/li[4]/a').click() # 재무 

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/span[2]/label').click() # 일반기업회계 

browser.find_element(By.ID, "forms").click() # 양식

browser.find_element(By.XPATH, '//*[@id="forms"]/option[2]').click() # 전계정 
'''
browser.find_element(By.ID, "range").click() # 범위 
browser.find_element(By.XPATH, '//*[@id="range"]/option[1]').click() # option[1] : 3년 option[2] : 5년
'''

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[1]/div/div[1]/div/div[7]/button').click() # 조회하기

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div[1]/div/div/button').click() #제무제표 다운로드
browser.find_element(By.LINK_TEXT, "손익계산서").click() 

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/button').click() #손익계산서 다운로드

browser.find_element(By.LINK_TEXT, "재무분석").click() 

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[4]/div/div[1]/div/div[2]/div[2]/div/span[2]/label').click() # 일반기업회계

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[4]/div/div[1]/div/div[2]/div[2]/div/span[2]/label').click() # 조회하기

browser.find_element(By.XPATH, '//*[@id="etfi110m1"]/div/div[3]/div/div/div/div[4]/div/div[2]/div[2]/div[1]/div/div/button').click() #재무분석 다운로드