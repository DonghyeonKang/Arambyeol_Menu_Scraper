import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
from typing import Dict, List, Tuple

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        db=os.environ.get('MYSQL_DATABASE', 'arambyeol'),
        charset='utf8mb4'
    )

def save_menu(menu_data: Dict[str, List[Tuple[str, str, List[str]]]]):
    """
    메뉴 데이터를 DB에 저장하는 함수
    Args:
        menu_data: {
            날짜: [(식사타입, 코스명, [메뉴항목들]), ...]
        }
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # menu 테이블에 메뉴 저장
            for date, meals in menu_data.items():
                for meal_type, course, items in meals:
                    # 메뉴 항목들을 하나의 문자열로 결합
                    menu_items = '\n'.join(items)
                    
                    # menu 테이블에 메뉴 저장
                    cursor.execute(
                        "INSERT INTO menu (menu, img_path) VALUES (%s, %s)",
                        (menu_items, '')  # img_path는 현재 미구현
                    )
                    menu_id = cursor.lastrowid
                    
                    # plan 테이블에 식단 정보 저장
                    cursor.execute(
                        "INSERT INTO plan (menu_id, date, course) VALUES (%s, %s, %s)",
                        (menu_id, date, course)
                    )
            
            conn.commit()
            print("Successfully saved menu data to database")
            
    except Exception as e:
        print(f"Error saving menu data: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

def fetch_menu_page():
    # Target URL
    url = "https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # # Send GET request to the URL
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()  # Raise an exception for bad status codes
        
        # # Create a directory for storing HTML files if it doesn't exist
        # os.makedirs('html_files', exist_ok=True)
        
        # # Use fixed filename
        # filename = 'html_files/menu.html'
        
        # # Save the HTML content
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(response.text)
            
        # print(f"Successfully saved HTML content to {filename}")
        return True
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return False

def parse_menu():
    try:
        with open('html_files/menu.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the table containing menu information
        table = soup.find('table')
        if not table:
            print("Could not find menu table")
            return
        
        # Get dates from table headers
        headers = table.find_all('th')
        dates = [header.text.strip() for header in headers[1:]]  # Skip first header (구분)
        
        # Dictionary to store all menu data
        menu_data = {}
        
        # Get menu rows
        rows = table.find_all('tr')
        
        # Process each meal type (아침, 점심, 저녁)
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if not cells:
                continue
                
            meal_type = cells[0].text.strip()  # 아침, 점심, 저녁
            if meal_type not in ['아침', '점심', '저녁']:
                continue
                
            print(f"\n=== {meal_type} ===")
            
            # Process each day's menu
            for date, cell in zip(dates, cells[1:]):
                if date not in menu_data:
                    menu_data[date] = []
                
                print(f"\n[{date}]")
                
                # Find all menu sections in the cell
                menu_sections = cell.find_all('div')
                for section in menu_sections:
                    # Get course title and menu items
                    title = section.find('p', class_='fm_tit_p')
                    menu_items = section.find_all('p')
                    
                    if title and menu_items:
                        course_title = title.text.strip()
                        print(f"\n{course_title}")
                        
                        # Get the menu items (skip the title)
                        menu_text = menu_items[-1].text.strip()  # Get the last p tag which contains the menu items
                        if menu_text and not menu_text.startswith('[공지]'):
                            items = []
                            menu_items = menu_text.split('\n')
                            for item in menu_items:
                                if item.strip():  # Only include non-empty items
                                    items.append(item.strip())
                                    print(f"- {item.strip()}")
                            
                            # Store menu data
                            menu_data[date].append((meal_type, course_title, items))

        # Save menu data to database
        save_menu(menu_data)

    except FileNotFoundError:
        print("Menu HTML file not found. Please run fetch_menu_page() first.")
    except Exception as e:
        print(f"Error parsing menu: {e}")

if __name__ == "__main__":
    # fetch_menu_page()  # Commented out as requested
    parse_menu()