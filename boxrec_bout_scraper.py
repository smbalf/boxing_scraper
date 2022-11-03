import requests
import re
from bs4 import BeautifulSoup
import csv

headers = {'User-Agent': 'Mozilla/5.0'}
boxrec_url = 'https://boxrec.com/en/box-pro/15243'
# Catching errors and printing

def launch_soup():
    try:
        response = requests.get(boxrec_url, headers=headers )
        response.raise_for_status()
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        response.encoding = 'utf-8'
        # Scrape the page!
        bs = BeautifulSoup(response.text, 'lxml')
        check_can_scrape(bs)

def check_can_scrape(soup):
    boxrec_tables = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)

    if access == 0:
        print('7.. 8.. 9.. 10! BOXREC KO!')
        print('Closing scripts...')
        exit()
    else:
        print(f'SCRAPING...')
        grab_table_data(soup)

def grab_table_data(soup):
# TODO
# Create a nest dict as below
#bout_data_dict = {
#    'url': {
#        'bout_date': date,
#        'bout_info': {
#            'opponent_url': opponent_url,
#            'opponent_wld': opponent_wld,
#            'result': result,
#            'round_ended': round_ended
#        }
#    }
#}
    bout_hist_table = soup.find_all('table', {'class': 'dataTable'})
    for table_value in bout_hist_table:
        date = table_value.find_all('a', href=re.compile('^(/en/date?)'))
        for dates in date:
            dates.get_text()
            


launch_soup()