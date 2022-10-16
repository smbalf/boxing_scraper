import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import time
import re


os.system('cls')


boxer_data = []
key_list = ['name']
dirty_value_list = []
clean_value_list = []


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
        clean_and_write_to_csv(dirty_value_list, clean_value_list)
        print('######################')
        print(f'DATA ROW ADDED {boxrec_url}')

def grab_boxer_data(soup):
    boxer_name = soup.find('h1').get_text()
    dirty_value_list.append(boxer_name)

    boxrec_tables = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)

    if access == 0:
        print('REROUT YOUR DAMN VPN')
        return None
    else:
        print('SCRAPING...')

    for table_value in boxrec_tables:
        first_td = table_value.find_all('b')
        print(f'SCRAPED {len(first_td)} DATA POINTS')
        for item in first_td:
            key = item.get_text()
            value = item.find_next().get_text()
            key_list.append(key)
            dirty_value_list.append(value)

def clean_and_write_to_csv(dirty_list, clean_list):
    print('CLEANING THE DATA...')
    no_pct = [pct.replace('%', '') for pct in dirty_list]
    no_slash_n = [whitespace.replace('\n', '') for whitespace in no_pct]
    no_fwd_slash = [fwd_slash.replace('/', '') for fwd_slash in no_slash_n]
    no_space = [whitespace.replace(' ', '') for whitespace in no_fwd_slash]
    no_xa0 = [xa0.replace('\xa0', '') for xa0 in no_space]
    no_comma = [comma.replace(',', ' ') for comma in no_xa0]
    for value in no_comma:
        clean_list.append(value)

    zip_iter = zip(key_list, clean_value_list)

    boxer_dict = dict(zip_iter)

    csv_headers = ['name', 'division', 'bouts', 'rounds', 'KOs', 'debut', 'age', 'stance', 'height', 'reach', 'residence', 'birth place']
    csv_values = [boxer_dict[header] for header in csv_headers]

    zip_csv = zip(csv_headers, csv_values)
    print('CREATED CSV DICTIONARY, FINAL CLEANING')
    csv_dict = dict(zip_csv)

    for item in csv_dict:
        if item == 'height':
            if csv_dict[item] != '':
                csv_dict[item] = csv_dict[item][-5:-2]
        elif item == 'reach':
            if csv_dict[item] != '':
                csv_dict[item] = csv_dict[item][-5:-2]
        elif item == 'name':
                split_name = re.findall('[A-Z][a-z]+', csv_dict[item])
                csv_dict[item] = ' '.join(split_name)
        if csv_dict[item] == '':
            csv_dict[item] = 'NODATA'

    with open('boxrec_tables.csv', 'a', encoding="utf-8", newline='') as boxrec_csv:
        writer = csv.DictWriter(boxrec_csv, fieldnames=csv_headers)
        print('WRITING TO CSV...')
        writer.writerow(csv_dict)



rotate_boxer_urls()

