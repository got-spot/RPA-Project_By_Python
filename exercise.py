import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_experimental_option('detach', True)

browser = webdriver.Chrome(options=options)

url = "https://dart.fss.or.kr/dsab007/main.do?option=corp"
browser.get(url)


browser.find_element(By.XPATH, '//*[@id="btnPlus"]').click()
browser.find_element(By.ID, "businessNm").click()
time.sleep(10) # 업종 선택시간

browser.find_element(By.XPATH, '//*[@id="maxResultsCb"]/option[4]').click() # 조회 100
browser.find_element(By.XPATH, '//*[@id="corporationType"]/option[2]').click() # 유가증권
browser.find_element(By.XPATH, '//*[@id="searchForm"]/div[2]/div[2]/a[1]').click() # 검색
time.sleep(3)


im = browser.find_element(By.XPATH, '//*[@id="tbody"]/tr[100]/td[2]/span/a')
print(im)




'''
for i in range(1, 101):
    try:
        xpath = '//*[@id="tbody"]/tr[{}]/td[2]/span/a'.format(i)
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        for elem in elements:
            elem.click()
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            corp = soup.select_one('#winCorpInfo > div.layerPop.layerPopM > div.cont > table > tbody > tr:nth-child(8) > td')
            com_num = corp.get_text()
            com_nums.append(com_num) # com_nums 리스트에 값 추가
            browser.find_element(By.LINK_TEXT, "닫기").click()
    except Exception as e:
        print(f'에러 발생: {e}')

# 전역 변수 com_nums는 이제 어디서든 사용 가능
 '''       
