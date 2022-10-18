# RANDOM FILE FOR TESTING SCRIPTS
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import csv
import time


key_list = ['name', 'division rating', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
dirty_value_list = []
clean_value_list = []
csv_headers = ['name', 'division rating', 'division', 'bouts', 'rounds', 'KOs', 'debut', 'age', 'stance', 'height', 'reach', 'residence', 'birth place', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
csv_dict = {}

def rotate_boxer_urls():
    global key_list
    global dirty_value_list
    global clean_value_list

    with open('boxrec_top_50_urls.csv', 'r') as top_50_urls_csv:
        reader = csv.reader(top_50_urls_csv)
        top_50_urls_list = []
        for row in reader:
            top_50_urls_list.append(', '.join(row))

    for url in top_50_urls_list:
        boxrec_url = 'https://boxrec.com' + url
        headers = {'User-Agent':'Mozilla/5.0'}

        try:
            response = requests.get(boxrec_url, headers = headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            
        else:
            response.encoding = 'utf-8' # Optional: requests infers this internally
            bs = BeautifulSoup(response.text, 'lxml')

            grab_boxer_data(bs)
            
            time.sleep(1)
            clean_data(dirty_value_list, clean_value_list)
            
            time.sleep(1)
            write_to_csv(csv_headers, csv_dict)
            
            key_list = ['name', 'division rating', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
            dirty_value_list = []
            clean_value_list = []

            print('---------------------------------------------')

def grab_boxer_data(soup):
    boxrec_tables = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)

    if access == 0:
        print('REROUT YOUR DAMN VPN')
        print('closing scraper...')
        exit()
    else:
        print('SCRAPING...')
        time.sleep(1.5)

    boxer_name = soup.find('h1').get_text()
    dirty_value_list.append(boxer_name)

    ratings = []
    for link in soup.find_all('a', href=re.compile('^(/en/ratings?)')):
        ratings.append(link.get_text())

    no_slash_n = [whitespace.replace('\n', '') for whitespace in ratings]
    no_space = [whitespace.replace(' ', '') for whitespace in no_slash_n]
    rating = no_space[1]
    division_rating = rating[1:3]
    dirty_value_list.append(division_rating)

    wins = soup.find('td', {'class': 'bgW'}).get_text()
    dirty_value_list.append(wins)
    losses = soup.find('td', {'class': 'bgL'}).get_text()
    dirty_value_list.append(losses)
    draws = soup.find('td', {'class': 'bgD'}).get_text()
    dirty_value_list.append(draws)
    ko_wins = soup.find('th', {'class': 'textWon'}).get_text()
    dirty_value_list.append(ko_wins[:-4])
    ko_losses = soup.find('th', {'class': 'textLost'}).get_text()
    dirty_value_list.append(ko_losses[:-4])

    for table_value in boxrec_tables:
        first_td = table_value.find_all('b')
        for item in first_td:
            key = item.get_text()
            value = item.find_next().get_text()
            key_list.append(key)
            dirty_value_list.append(value)
            
            if item.get_text() == 'reach':
                print('found reach')
                value_reach = item.find_next().find_next().find_next()
                boxer_reach = value_reach.get_text()
                key_list.append(key)
                dirty_value_list.append(boxer_reach)


def clean_data(dirty_list, clean_list):
    global csv_headers
    global csv_dict

    print('CLEANING THE DATA...')
    time.sleep(1.5)
    no_pct = [pct.replace('%', '') for pct in dirty_list]
    no_slash_n = [whitespace.replace('\n', '') for whitespace in no_pct]
    no_fwd_slash = [fwd_slash.replace('/', '') for fwd_slash in no_slash_n]
    no_space = [whitespace.replace(' ', '') for whitespace in no_fwd_slash]
    no_xa0 = [xa0.replace('\xa0', '') for xa0 in no_space]
    no_comma = [comma.replace(',', ' ') for comma in no_xa0]
    for value in no_comma:
        clean_list.append(value)

    if key_list[20] != 'reach':
        key_list.insert(20, 'reach')
        clean_value_list.insert(20, '')

    boxer_dict = dict(zip(key_list, clean_value_list))
    csv_values = [boxer_dict[header] for header in csv_headers]
    csv_dict = dict(zip(csv_headers, csv_values))
    print('CREATED CSV DICTIONARY, FINAL CLEANING')
    time.sleep(1.5)
    

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
        elif item == 'residence':
                split_name = re.findall('[A-Z][a-z]+', csv_dict[item])
                csv_dict[item] = ' '.join(split_name)
        elif item == 'birth place':
                split_name = re.findall('[A-Z][a-z]+', csv_dict[item])
                csv_dict[item] = ' '.join(split_name)
        if csv_dict[item] == '':
            csv_dict[item] = 'NODATA'

        print('DATA CLEANED')


def write_to_csv(csv_header=csv_headers, csv_dict=csv_dict):
    with open('test.csv', 'a', encoding="utf-8", newline='') as boxrec_csv:
        writer = csv.DictWriter(boxrec_csv, fieldnames=csv_headers)
        print('WRITING TO CSV...')
        writer.writerow(csv_dict)


rotate_boxer_urls()
