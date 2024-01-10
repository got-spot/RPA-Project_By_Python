import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option('detach', True)

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

url = "https://dart.fss.or.kr/dsab007/main.do?option=corp"
browser.get(url)


browser.find_element(By.XPATH, '//*[@id="btnPlus"]').click()
browser.find_element(By.ID, "businessNm").click()

# browser.find_element(By.XPATH, '//*[@id="root4747"]/i').click() # 업종 선택 부분
# browser.find_element(By.XPATH, '//*[@id="46"]/i').click() # 업종 선택 부분
# browser.find_element(By.ID, "467_anchor").click() # 업종 선택 부분

time.sleep(10) # 업종 선택시간

browser.find_element(By.XPATH, '//*[@id="maxResultsCb"]/option[4]').click() # 조회 100
browser.find_element(By.XPATH, '//*[@id="corporationType"]/option[2]').click() # 유가증권시장
browser.find_element(By.XPATH, '//*[@id="searchForm"]/div[2]/div[2]/a[1]').click() # 검색
time.sleep(3)

com_nums = [] # 사업자 등록번호 list


# 페이지 로딩 대기
wait = WebDriverWait(browser, 10)
soup = BeautifulSoup(browser.page_source, 'html.parser')
numOfpage = soup.css.select("#psWrap > div.pageSkip > ul > li > a")
# name_xpath = '//*[@id="tbody"]/tr[1]/td[2]/span/a' # 업체명 xpath
# elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, name_xpath)))

# 각 페이지 첫 번째 업체명만 갖고 오는 반복문
for i in range(len(numOfpage)):
    page_xpath = '//*[@id="psWrap"]/div[2]/ul/li[{}]/a'.format(i+1) # 다음 페이지 이동 xpath

    browser.find_element(By.XPATH, '//*[@id="tbody"]/tr[1]/td[2]/span/a').send_keys(Keys.ENTER) # 첫 번째 업체 클릭
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    corp = soup.select_one('#winCorpInfo > div.layerPop.layerPopM > div.cont > table > tbody > tr:nth-child(8) > td')
    com_num = corp.get_text()

    # com_nums 리스트에 값이 이미 있는 경우 continue 
    if com_num in com_nums:
        continue
    else:
        com_nums.append(com_num)

    browser.find_element(By.XPATH, '//*[@id="winCorpInfo"]/div[4]/div[1]/a').click() # 닫기 버튼 클릭
    time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 페이지 하단으로 이동
    time.sleep(1)
    # 다음 페이지 이동
    browser.find_element(By.XPATH, page_xpath).click()
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 0)") # 페이지 상단으로 이동
    time.sleep(1)

print(com_nums)
# browser.find_element(By.XPATH, '//*[@id="psWrap"]/div[2]/ul/li[3]/a').click()
'''
soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.find_element(By.LINK_TEXT, '6').click() # 6페이지 이동
time.sleep(3)
numOfpage = soup.css.select("#psWrap > div.pageSkip > ul > li > a") # dart 페이지 갯수


numOfcorp = soup.css.select("#tbody > tr > td > span > a") # 현재 페이지의 업체명 갯수 '''
