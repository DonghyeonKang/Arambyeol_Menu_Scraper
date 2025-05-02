from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-pipe')
chrome_options.binary_location = '/usr/bin/google-chrome'

service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# 페이지 요청
url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"
driver.get(url)

# ✅ 무조건 5초 대기 (렌더링 여유 확보)
time.sleep(5)

# 이후 처리
aram_html = driver.page_source
with open("html_code.txt", "w", encoding="utf-8") as file:
    file.write(aram_html)

driver.quit()

# BeautifulSoup 파싱
soup = BeautifulSoup(aram_html, 'html.parser')


