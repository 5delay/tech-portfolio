import time
import csv
import argparse
import os
import sys
from datetime import datetime
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')
)
sys.path.append(PROJECT_ROOT)
from utils.utils import *
import random

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save_format", type=str, choices=["csv", "mysql"], default="mysql")
    parser.add_argument("-u", "--url", type=str) #required=True 제거
    args = parser.parse_args()
    
    return args

def main(args):
    main_page_url = 'https://www.hospitalitynet.org'

    year_ago_date = Get_Date_from_a_Year_ago()
    date_format = "%Y-%m-%dT%H:%M:%S"
    year_ago_date = year_ago_date.strftime(date_format)
    year_ago_datetime = datetime.strptime(year_ago_date, date_format)

    all_article_urls = []
    article_num = 1

    while True:
        url = f'{main_page_url}/list/{article_num}-{article_num+9}/{args.url}/all-latest-news.html'
        print(f"현재 페이지: {url}")
        soup = Load_soup(url)
        time.sleep(random.uniform(2,4))

        article_tags = soup.find_all('article', attrs={'class':'list-item'})
        article_urls = [main_page_url+article_tag.find('a', attrs={'class':'gaa'})['href'] for article_tag in article_tags]

        all_article_urls.extend(article_urls)
        print("크롤링할 아티클 개수: ", len(all_article_urls))
        time_tags = [article_tag.find('time') or article_tag.find('timeago') for article_tag in article_tags]
        crawled_times = sorted([time_tag['datetime'].split('+')[0] for time_tag in time_tags])
        try:
            crawled_datetime = datetime.strptime(crawled_times[-1], date_format)
        except: #마지막 페이지에 아티클이 없는 경우 이전 페이지의 crawled_datetime 이용
            pass 

        time.sleep(random.uniform(2,4))
        if crawled_datetime <= year_ago_datetime:
            break
        else:
            try:
                article_num += 10
                next_url = f'{main_page_url}/list/{article_num}-{article_num+9}/{args.url}/all-latest-news.html'
                soup = Load_soup(next_url)
            except Exception as e:
                print("CANNOT GET NEXT PAGE ! \n", e)
                break

    ''' 4. Crawl the content of each article '''
    for article_url in all_article_urls:
        print("url: ", article_url)
        soup = Load_soup(article_url)
        time.sleep(1)
        year_ago_date = Get_Date_from_a_Year_ago()
        date_format = "%d %b %Y %H:%M:%S"
        year_ago_date = year_ago_date.strftime(date_format)
        year_ago_datetime = datetime.strptime(year_ago_date, date_format)

        vertical = 'Hospitality'
        site = 'Hospitalitynet'
        format = 'News'
        if args.url in ["opinion", "viewpoint", "report", "whitepaper", 'view-with-article']: # view-with-article도 동명의 opinion 탭
            format = 'Expertise'

        # title
        try: 
            title = soup.find('div', class_='title').find('h1').text
            if not title.strip():
                print("제목이 없는 기사입니다.")
                continue
        except Exception as e:
            print(f"Error processing URL {article_url}: {e}")
            continue
        print("기사 제목: ", title)
        
        # upload date
        date = soup.find('meta', {'name': 'last-modified'}).get('content').strip().split(", ")[1].replace(" GMT", "")
        upload_date = datetime.strptime(date, date_format)
        print("업로드 날짜:", upload_date)
        if upload_date <= year_ago_datetime:
            continue

        # content
        content_body = soup.find('div', class_='formatted')
        content_tags = content_body.find_all(['p', 'h3']) # 태그 종류에 상관없이 순서대로 수집
        filtered_content_tags = []
        for tag in content_tags:
            text = tag.get_text(strip=True)
            if 'Photo by' in text:
                continue
            if 'The Hotel Yearbook' in text or 'Hospitality ESG Edition' in text: # yearbook의 최하단에 나오는 광고성 내용 제외
                break
            filtered_content_tags.append(tag)
        content = ' '.join(tag.get_text(strip=True) for tag in filtered_content_tags)
        content = Clean_Text(content)

        ''' 5. Save Data '''
        if args.save_format == "csv":
            writer.writerow([vertical, site, format, title, content, '', '', upload_date, article_url, '', '', ''])
        # elif args.save_format == "mysql":
            # Save_to_MySQL(vertical, site, format, title, content, '', '', upload_date, article_url, '', '', '')

    print("수집 완료한 아티클 개수: ", len(all_article_urls))
    print(f"\n Data saved successfully in {args.save_format}")

if __name__ == '__main__':
    args = parse_arg()

    if args.save_format == "csv":
        csv_path = f"{PROJECT_ROOT}/csv_results/hospitalitynet"
        os.makedirs(csv_path, exist_ok=True)
        csv_save_path = f'{csv_path}/{args.url}.csv'
        f = open(csv_save_path, "w", encoding="utf-8", newline="")
        writer = csv.writer(f)
        writer.writerow(["Vertical", "Site", "Format", "Title", "Content", "Title-Kor", "Content-Kor", "Upload_Date", "URL", "Keyword", "Sentiment"])
    main(args)
    
    if args.save_format == "csv":
        f.close()