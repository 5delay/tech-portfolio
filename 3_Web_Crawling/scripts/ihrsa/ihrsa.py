import time
import csv
import argparse
import os
import sys
from datetime import datetime, timedelta
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
    ''' 0. Webpage URL for crawling '''
    url = f"https://www.ihrsa.org/improve-your-club/topic/{args.url}/"
    print(f"Now Crawling {url} !!! ")

    ''' 1. Load Chrome Driver to use Selenium & Parsing to bs4 object after HTTP GET request '''

    # soup = BeautifulSoup(driver.page_source, "html.parser")
    soup = Load_soup(url)
    
    ''' 2. Get the date 1 year ago using func in utils.py '''
    year_ago_date = Get_Date_from_a_Year_ago()
    
    ## Formatting according to the Upload date format for each site !!!
    #ex) August 23, 2023
    date_format = "%B %d, %Y"
    year_ago_date = year_ago_date.strftime(date_format)
    year_ago_datetime = datetime.strptime(year_ago_date, date_format)

    print("2년 전 date :", year_ago_datetime)

    ''' 3. Collect 1 year worth of article urls '''
    ### Load more articles btn click to find crawling article for 1 year article
    ''' Site-Specific article url collection code ... '''
    
    article_urls = []
    time.sleep(15)

    # big thumbs 1개
    thumb = soup.select_one('section.masthead h3 a')
    if thumb:
        article_urls.append(thumb.get('href'))

    # 아래의 모든 기사
    articles = soup.find_all('li', class_ = 'col-sm-4 feat-box')
    article_urls += [article.select_one('li a').get('href') for article in articles]

    print(f"num of crawling articles : {len(article_urls)}")
    time.sleep(2)

    ''' 4. Crawl the content of each article '''
    for article in article_urls:
        
        soup = Load_soup(article)
        time.sleep(2)
        
        vertical = 'Hospitality'
        format = 'Expertise'

        # title
        title = soup.find('meta', attrs = {'property':'og:title'})['content']

        # upload_date
        try:
            crawled_date  = soup.select('ul.topic-breadcrumb.art-date li')[1].text        
        except:
            crawled_date  = soup.select_one('ul.topic-breadcrumb.art-date li').text
        
        upload_date = datetime.strptime(crawled_date, date_format)

        if upload_date <= year_ago_datetime: continue
        
        # content
        content = ''
        
        single_content = soup.find_all('div', class_ = ['body-content pb', 'body-content'])
        for single in single_content:
            p_tags = single.find_all('p')
            for p in p_tags:
                content += p.text+' '
                        
            h4_tags = single.find_all('h4')
            for h4 in h4_tags:
                content += h4.text+' '
        
            li_tags = single.select('ul li')
            for li in li_tags:
                content += li.text+' '
                
            lip_tags = single.select('ol li p')
            for lip in lip_tags:
                content += lip.text+' '
    
       
        ''' 5. Save Data '''
        if args.save_format == "csv":
            writer.writerow([vertical, 'ihrsa', format, title, content, '', '', upload_date, article, '', '', ''])            
        # elif args.save_format == "mysql":
        #     Save_to_MySQL(vertical, 'ihrsa', format, title, content, '', '', upload_date, article, '', '', '')
    
    print(f"\n Data saved successfully {args.url} !!!\n")

if __name__ == '__main__':
    args = parse_arg()
    
    # If you want to save the data to csv file ,
    if args.save_format == "csv":
        os.makedirs(f'{PROJECT_ROOT}/csv_results/ihrsa/', exist_ok=True)
        csv_save_path = f'{PROJECT_ROOT}/csv_results/ihrsa/{args.url}.csv'
        f = open(csv_save_path, "w", encoding="utf-8", newline="")
        writer = csv.writer(f)
        writer.writerow(["Vertical", "Site", "Format", "Title", "Content", "Title-Kor", "Content-Kor", "Upload_Date", "URL", "Keyword", "Sentiment"])

    main(args)

    if args.save_format == "csv": f.close()