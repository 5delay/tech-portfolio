from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import pymysql
from datetime import datetime, timedelta
import os


def Clean_Text(text):
    cleaned_text = text.strip()
    cleaned_text = '\n'.join(line.strip() for line in cleaned_text.splitlines() if line.strip())
    return cleaned_text
    
# selenium
def Load_Driver():
    driver_path = "/usr/local/bin/chromedriver"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver

# bs4
def Load_soup(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # Get url
    response = requests.get(url, headers=headers)
    # 200번대 코드가 아니면 코드 멈춤
    response.raise_for_status() 
    # 응답받은 text를 HTML 파싱
    html = response.text
    # 웹 페이지의 HTML 내용을 BeautifulSoup 객체로 파싱
    soup = BeautifulSoup(html, "html.parser")

    return soup

def Get_Date_from_a_Year_ago():
    date_year_ago = datetime.now() - timedelta(days=365) # 오늘로부터 1년전 -> 3년전으로 변경
    date_year_ago = date_year_ago.replace(hour=0, minute=0, second=0, microsecond=0) #시간은 자정으로 설정

    return date_year_ago

           
def errorLog(error_message, url):
    error_log_path = f'./error_log.txt'
    with open(error_log_path, 'a', encoding='utf-8') as error_log:
        error_log.write(f"Error: {error_message}\n")
        error_log.write(f"URL: {url}\n")
        error_log.write(f"Timestamp: {datetime.now()}\n")
        error_log.write("=" * 50 + "\n")




# def connect_to_mysql():
#     # Database connection parameters
#     db_config = {
#         'host': 'mysql',
#         'user': 'lge',
#         'password': 'lge2023',
#         'database': 'lge'
#     }

#     # Connect to the database
#     connection = pymysql.connect(**db_config)
#     return connection

# def is_db_exists(cursor):
#     table_name = 'Article'

#     # Create table if it is not exists
#     create_table_sql = f"""
#     CREATE TABLE IF NOT EXISTS {table_name}(
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         Vertical VARCHAR(50),
#         Site VARCHAR(50),
#         Article_Format VARCHAR(50),
#         Title TEXT,
#         Content LONGTEXT,
#         Title_Kor VARCHAR(600),
#         Content_Kor VARCHAR(600),
#         Upload_Date VARCHAR(50),
#         URL VARCHAR(255),
#         Keyword LONGTEXT,
#         Title_Sentiment VARCHAR(255),
#         Content_Sentiment VARCHAR(255)
#     )
#     """
#     cursor.execute(create_table_sql)
#     return 0


# def is_data_exists(cursor, table_name, title, content):
#     # Check if data with the given Title or Content already exists
#     check_data_sql = f"SELECT Id FROM {table_name} WHERE Title = %s OR Content = %s"
#     cursor.execute(check_data_sql, (title, content))
#     return cursor.fetchone()
    
# def Save_to_MySQL(vertical, site, format, title, content, title_kor, content_kor, upload_date, article_url, keyword, title_sentiment, content_sentiment):
#     connection = connect_to_mysql()
    
#     table_name = 'Article'
    
#     try:
#         with connection.cursor() as cursor:
#             is_db_exists(cursor)
            
#             result = is_data_exists(cursor, table_name, title, content)

#             # 중복 데이터 존재
#             if result:
#                 pass
#             # 중복 데이터가 존재하지 않으면
#             else:
#                 insert_data_sql = f"""
#                 INSERT INTO {table_name} 
#                 (Vertical, Site, Article_Format, Title, Content, Title_Kor, Content_Kor, Upload_Date, URL, Keyword, Title_Sentiment, Content_Sentiment) 
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(insert_data_sql, (vertical, site, format, title, content, title_kor, content_kor, upload_date, article_url, keyword, title_sentiment, content_sentiment))
#                 # 변경사항 커밋
#                 connection.commit()

#     except Exception as e:
#         print("MySQL에 데이터를 저장하는데 실패했습니다.", e)

#     finally:
#         connection.close()
#     return 0