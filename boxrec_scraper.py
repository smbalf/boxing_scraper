import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import time


os.system('cls')

boxrec_url = 'https://boxrec.com/en/box-pro/356831' 

req = Request(boxrec_url, headers={'User-Agent':'Mozilla/5.0'})
html = urlopen(req)
bs = BeautifulSoup(html.read(), 'html.parser')

boxer_data = []

def rotate_boxer_urls():
    with open('boxrec_top_50_urls.csv', 'r') as top_50_urls_csv:
        reader = csv.reader(top_50_urls_csv)
        top_50_urls_list = []
        for row in reader:
            top_50_urls_list.append(', '.join(row))

    for url in top_50_urls_list:
        boxrec_url = 'https://boxrec.com' + url
        print(boxrec_url)
        req = Request(boxrec_url, headers={'User-Agent':'Mozilla/5.0'})
        html = urlopen(req)
        bs = BeautifulSoup(html.read(), 'html.parser')
        grab_boxer_data(bs)
        time.sleep(2)

def grab_boxer_data(soup):
    data_list  = []
    boxer_name = soup.find('h1').get_text()
    data_list.append(boxer_name)
    boxrec_data = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_data)
    x = 0
    if access == 0:
        print('REROUT YOUR DAMN VPN')
        return None
    else:
        print('SCRAPING...')

    scrape_list = [1, 7, 9, 11, 15, 27, 31, 33, 35, 37, 39]
    for data in boxrec_data:
        parent_element = data.parent
        parent_text = parent_element.find_all('td')
        for parent_data in parent_text:
            if x in scrape_list:
                data_list.append(parent_data.get_text())
            else:
                pass
            x += 1

    no_pct = [pct.replace('%', '') for pct in data_list]
    no_slash_n = [whitespace.replace('\n', '') for whitespace in no_pct]
    no_space = [whitespace.replace(' ', '') for whitespace in no_slash_n]
    no_comma = [comma.replace(',', ' ') for comma in no_space]
    clean_list = no_comma

    xx = 0
    for item in clean_list:
        if xx == 8 or xx == 9:
            boxer_data.append(item[-5:-2])
        else:
            boxer_data.append(item)
        xx += 1

    print(f'adding {len(boxer_data)} data points to csv...')
    print(boxer_data)

    with open('boxrec_tables.csv', 'a', newline='') as boxrec_csv:
        writer = csv.writer(boxrec_csv)
        writer.writerow(boxer_data)
    print('CSV CREATED')



rotate_boxer_urls()