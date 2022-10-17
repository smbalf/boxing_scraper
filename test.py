# RANDOM FILE FOR TESTING SCRIPTS


import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import re


os.system('cls')


boxrec_url = 'https://boxrec.com/en/box-pro/724390'

req = Request(boxrec_url, headers={'User-Agent':'Mozilla/5.0'})
html = urlopen(req)
bs = BeautifulSoup(html.read(), 'html.parser')
boxer_name = bs.find('h1').get_text()

ratings = []
for link in bs.find_all('a', href=re.compile('^(/en/ratings?)')):
    ratings.append(link.get_text())

no_slash_n = [whitespace.replace('\n', '') for whitespace in ratings]
no_space = [whitespace.replace(' ', '') for whitespace in no_slash_n]
rating = no_space[1]
division_rating = rating[1:3]

boxrec_tables = bs.find_all('td', {'class': 'rowLabel'})

key_list = ['name', 'division rating']
dirty_value_list = []
dirty_value_list.append(boxer_name)
dirty_value_list.append(division_rating)

clean_value_list = []


for table_value in boxrec_tables:
    first_td = table_value.find_all('b')
    for item in first_td:
        key = item.get_text()
        value = item.find_next().get_text()
        key_list.append(key)
        dirty_value_list.append(value)

def clean_data(dirty_list, clean_list):
    no_pct = [pct.replace('%', '') for pct in dirty_list]
    no_slash_n = [whitespace.replace('\n', '') for whitespace in no_pct]
    no_fwd_slash = [fwd_slash.replace('/', '') for fwd_slash in no_slash_n]
    no_space = [whitespace.replace(' ', '') for whitespace in no_fwd_slash]
    no_xa0 = [xa0.replace('\xa0', '') for xa0 in no_space]
    no_comma = [comma.replace(',', ' ') for comma in no_xa0]
    for value in no_comma:
        clean_list.append(value)

clean_data(dirty_value_list, clean_value_list)

if key_list[16] == 'reach':
    zip_iter = zip(key_list, clean_value_list)
elif key_list[16] != 'reach':
    key_list.insert(16, 'reach')
    clean_value_list.insert(16, '')

boxer_dict = dict(zip(key_list, clean_value_list))

print(boxer_dict)

csv_headers = ['name', 'division rating', 'division', 'bouts', 'rounds', 'KOs', 'debut', 'age', 'stance', 'height', 'reach', 'residence', 'birth place']
csv_values = [boxer_dict[header] for header in csv_headers]

csv_dict = dict(zip(csv_headers, csv_values))
print('CREATED CSV DICTIONARY, FINAL CLEANING')
print(csv_dict)

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

print(csv_dict)
with open('boxrec_tables.csv', 'a', encoding="utf-8", newline='') as boxrec_csv:
    writer = csv.DictWriter(boxrec_csv, fieldnames=csv_headers)
    writer.writerow(csv_dict)




