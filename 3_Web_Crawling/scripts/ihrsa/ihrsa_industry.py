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
    url = f"https://www.ihrsa.org/improve-your-club/{args.url}"
    print(f"Now Crawling {url}")

    
    ''' 1. Parsing to bs4 object after HTTP GET request using func in utils.py '''
    soup = Load_soup(url)
    
    
    ''' 2. Get the date 1 year ago using func in utils.py '''
    year_ago_date = Get_Date_from_a_Year_ago()
    
    ## Formatting according to the Upload date format for each site !!!
    #ex) Aug 16, 2022
    date_format = "%B %d, %Y"
    year_ago_date = year_ago_date.strftime(date_format)
    year_ago_datetime = datetime.strptime(year_ago_date, date_format)

    print("2년 전 date :", year_ago_datetime)
    
    ''' 3. Collect 1 year worth of article urls '''
    article_urls = []
    next_page=1
    
    while True:
        time.sleep(2)
        
        ''' Site-Specific article url collection code ... '''
        ## 3-0. Get article url in the current main page
        hrefs = soup.find_all('div', class_ = 'col-sm-5')
        article_urls += [href.find('a')['href'] for href in hrefs]
        
        ## 3-1. Find the crawled_date, the upload date of the last crawled article
        last_article = article_urls[-1]
        soup = Load_soup(last_article)
        crawled_date  = soup.select('ul.topic-breadcrumb.art-date li')[1].text        
        crawled_datetime = datetime.strptime(crawled_date, date_format)

        time.sleep(2)
        ## 3-2. Compare last crawled_date with year_ago_date
        if crawled_datetime <= year_ago_datetime: break
        else:
            ## Get next page
            try:
                next_page += 1
                next_url = f'https://www.ihrsa.org/improve-your-club/{args.url}/p{next_page}/'
                
                soup = Load_soup(next_url)
        
            except Exception as e:
                print("CANNOT GET NEXT PAGE ! \n", e)

    print(f"num of crawling articles : {len(article_urls)}")
    
    ''' 4. Crawl the content of each article '''
    for article in article_urls:
        time.sleep(2)
        soup = Load_soup(article)
        
        vertical = 'Retail'
        format = 'Expertise'

        # title
        title = soup.find('meta', attrs = {'property':'og:title'})['content']

        # upload_date
        try:
            crawled_date  = soup.select('ul.topic-breadcrumb.art-date li')[1].text        
        except:
            crawled_date  = soup.select('ul.topic-breadcrumb.art-date li')[0].text   
        
        upload_date = datetime.strptime(crawled_date, date_format)

        if upload_date <= year_ago_datetime: continue

        # content
        content = ''
        
        single_content = soup.find('div', class_ = 'main-container news')

        p_tags = single_content.find_all('p')
        for p in p_tags:
            content += p.text+' '
                
        h4_tags = single_content.find_all('h4')
        for h4 in h4_tags:
            content += h4.text+' '

        li_tags = single_content.select('ul li p')
        for li in li_tags:
            content += li.text+' '


        ''' 5. Save Data '''
        if args.save_format == "csv":
            writer.writerow([vertical, 'ihrsa', format, title, content, '', '', upload_date, article, '', '', ''])            
        # elif args.save_format == "mysql":
        #     Save_to_MySQL(vertical, 'ihrsa', format, title, content, '', '', upload_date, article, '', '', '')
    
    print(f"\n Data saved successfully in {args.save_format}")


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