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
wait = WebDriverWait(browser, 10)

url = "https://dart.fss.or.kr/dsab007/main.do?option=corp"
browser.get(url)


browser.find_element(By.XPATH, '//*[@id="btnPlus"]').click()
browser.find_element(By.ID, "businessNm").click()
time.sleep(10) # 업종 선택시간

browser.find_element(By.XPATH, '//*[@id="maxResultsCb"]/option[4]').click() # 조회 100
browser.find_element(By.XPATH, '//*[@id="corporationType"]/option[2]').click() # 유가증권시장
browser.find_element(By.XPATH, '//*[@id="searchForm"]/div[2]/div[2]/a[1]').click() # 검색
time.sleep(3)

com_nums = [] # 사업자 등록번호 list

page = 1

while True:
    try:
        # 페이지 로딩 대기
        wait = WebDriverWait(browser, 10)
        name_xpath = '//*[@id="tbody"]/tr[{}]/td[2]/span/a'.format(i) # 업체명 xpath
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, name_xpath)))
        page_xpath = '//*[@id="psWrap"]/div[2]/ul/li[{}]/a'.format(i+1) # 다음 페이지 이동 xpath

        # 요소가 100개 미만일 경우, 끝 요소까지 반복 후 탈출
        for i in range(len(elements)):
            elem = elements[i]
            elem.click()
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            corp = soup.select_one('#winCorpInfo > div.layerPop.layerPopM > div.cont > table > tbody > tr:nth-child(8) > td')
            com_num = corp.get_text()

            # com_nums 리스트에 값이 이미 있는 경우 continue
            if com_num in com_nums:
                continue
            else:
                com_nums.append(com_num)

            browser.find_element(By.LINK_TEXT, "닫기").click()

        # 다음 페이지 이동
        browser.find_element(By.XPATH, page_xpath).click()
        page += 1

    except Exception as e:
        print('페이지 끝')
        break

# print(len(com_nums))