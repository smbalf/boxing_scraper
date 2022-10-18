# ANOTHER TEST FILE

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import csv
from urllib.request import urlopen, Request
import time


url_list = ['/en/box-pro/659772']
for url in url_list:
    boxrec_url = 'https://boxrec.com' + url
    headers = {'User-Agent':'Mozilla/5.0'}
    print(boxrec_url)

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


        boxrec_tables = bs.find_all('td', {'class': 'rowLabel'})

        for table_value in boxrec_tables:
            first_td = table_value.find_all('b')
            for item in first_td:
                if item.get_text() == 'reach':
                    value_reach = item.find_next().find_next().find_next()
                    print(value_reach.get_text()[-5:-2])