import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv


os.system('cls')

boxrec_url = 'https://boxrec.com/en/box-pro/356831' # GGG's url // will replace with loop

req = Request(boxrec_url, headers={'User-Agent':'Mozilla/5.0'})
html = urlopen(req)
bs = BeautifulSoup(html.read(), 'html.parser')

table_text = ['name']

def create_boxrec_csv():
    print('--FINDING TABLES--')
    boxrec_tables = bs.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)
    if access == 0:
        print('REROUT YOUR DAMN VPN')
        return
    x = 0
    skip = [1, 2, 6, 8, 9, 10, 11, 12, 14, 20, 21, 22]
    
    print('--WRANGLING--')
    for table_item in boxrec_tables:
        if x not in skip and x != 17:
            table_text.append(table_item.get_text())
        if x == 17:
            table_text.append(table_item.get_text()[0:-4])
        if x == (len(boxrec_tables) - 1):
            print('END OF TABLE DATA')
        x += 1

    print(table_text)

    print('--WRITING TO CSV--')
    with open('boxrec_tables.csv', 'wt+', newline='') as boxrec_csv:
        writer = csv.writer(boxrec_csv)
        writer.writerow(table_text)
    print('CSV CREATED')

create_boxrec_csv()
