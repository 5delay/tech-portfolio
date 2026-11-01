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

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save_format", type=str, choices=["csv", "mysql"], default="mysql")
    parser.add_argument("-u", "--url", type=str, required=True) 
    args = parser.parse_args()
    
    return args

def main(args):
    url = f"https://www.vendingtimes.com/topics/{args.url}/news/"

    print(f'Now Crawling {url}')
    soup = Load_soup(url)

    year_ago_date = Get_Date_from_a_Year_ago()

    date_format = "%Y-%m-%dT%H:%M:%S"
    year_ago_date = year_ago_date.strftime(date_format)
    year_ago_datetime = datetime.strptime(year_ago_date, date_format)


    article_urls = []    
    next_page=1
    
    while True:
        rows = soup.find_all('div', attrs={'class':'row fit'})
        
        article_urls += [row.find('a', class_='block')['href'] for row in rows]
        crawled_date = rows[-1].find('time')['datetime']
        crawled_datetime = datetime.strptime(crawled_date, date_format+"%z").replace(tzinfo=None)
        
        time.sleep(2)
        if crawled_datetime <= year_ago_datetime: break
        else:
            try:
                next_page += 1
                next_url = f'{url}/?page={next_page}'
                
                soup = Load_soup(next_url)
            except Exception as e:
                print("CANNOT GET NEXT PAGE ! \n", e)

    
    for article in article_urls:
        time.sleep(2)
        
        article = 'https://www.vendingtimes.com/'+ article
        
        soup = Load_soup(article)
        
        vertical = 'Retail'
        site = 'Vending Times'
        format = 'News' # News/Expertise
        
        title = soup.find('h1').text
        
        upload_date = soup.find('time')['datetime']
        upload_date = datetime.strptime(upload_date, date_format+"%z").replace(tzinfo=None)

        if upload_date <= year_ago_datetime: continue
        
        content = ''
        
        p_tags = soup.find('div', class_='description').find_all('p')
        for p in p_tags:
            content += p.text

        content = Clean_Text(content)

        ''' 5. Save Data '''
        if args.save_format == "csv":
            writer.writerow([vertical, site, format, title, content, '', '', upload_date, article, '', '', ''])
        # elif args.save_format == "mysql":
        #     Save_to_MySQL(vertical, site, format, title, content, '', '', upload_date, article, '', '', '')

    print(f"Data saved successfully in {args.save_format}\n")


if __name__ == '__main__':
    args = parse_arg()

    if args.save_format == "csv":
        os.makedirs(f'{PROJECT_ROOT}/csv_results/vendingtimes/', exist_ok=True)
        csv_save_path = f'{PROJECT_ROOT}/csv_results/vendingtimes/{args.url}.csv'
        f = open(csv_save_path, "w", encoding="utf-8", newline="")
        writer = csv.writer(f)
        writer.writerow(["Vertical", "Site", "Format", "Title", "Content", "Title-Kor", "Content-Kor", "Upload_Date", "URL", "Keyword", "Sentiment"])
    main(args)
    
    if args.save_format == "csv":
        f.close()
    