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

# 날짜 정보 추출 및 딕셔너리로 변환
day_date = {}
days = ['월', '화', '수', '목', '금', '토', '일']

th_tags = soup.find_all('th')  # <th> 태그 찾기

for th_tag in th_tags[1:8]:
    day = th_tag.contents[0].strip()  # 요일 
    date = th_tag.find('br').next_sibling  # <br> 태그 다음 텍스트 노드 추출
    if date is not None:
        date = date.strip()
        day_date[day] = date

menu_html = soup.find('tbody')
all_menulist = menu_html.find_all('tr')

morning_html = all_menulist[0].find_all('td')
lunch_html = all_menulist[1].find_all('td')
dinner_html = all_menulist[2].find_all('td')

