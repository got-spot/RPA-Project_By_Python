import os
os.system('pip install --upgrade selenium') # selenium 항상 최신버전 유지
# pip install beautifulsoup4
# pip install lxml

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지 옵션
browser = webdriver.Chrome(options=options)

browser.get("https://new.cretop.com/?h=1702989839177") # 크레탑으로 이동

