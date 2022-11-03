import requests
from bs4 import BeautifulSoup
import csv


def grab_table_data(soup):
    boxrec_tables = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)

    if access == 0:
        print('7.. 8.. 9.. 10! BOXREC KO!')
        print('Closing scripts...')
        exit()
    else:
        print(f'SCRAPING...')
    
    bout_hist_table = soup.find_all('table', {'class': 'dataTable'})
    for table_value in bout_hist_table:
        first_td = table_value.find_all('td')
        with open('bout_hist_table.txt', 'w') as f:
            for item in first_td:
                f.write(item.get_text())

headers = {'User-Agent': 'Mozilla/5.0'}
boxrec_url = 'https://boxrec.com/en/box-pro/15243'
# Catching errors and printing

try:
    response = requests.get(boxrec_url, headers=headers )
    response.raise_for_status()
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    response.encoding = 'utf-8'
    # Scrape the page!
    bs = BeautifulSoup(response.text, 'lxml')
    grab_table_data(bs)

