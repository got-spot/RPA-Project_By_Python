import csv, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option('detach', True)

browser = webdriver.Chrome(options=options)
url = "https://dart.fss.or.kr/dsab007/main.do?option=corp"
browser.get(url)

filename = "재무재표.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
soup = BeautifulSoup(browser.page_source, "lxml")

data_rows = soup.find("table", attrs={"class":"details"}).find("tbody").find_all("tr")
for row in data_rows:
    columns = row.find_all("td")
    data = [column.get_text() for column in columns]
    writer.writerow(data)
