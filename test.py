# RANDOM FILE FOR TESTING SCRIPTS

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

boxrec_url = 'https://boxrec.com/en/box-pro/356831'
headers = {'User-Agent':'Mozilla/5.0'}

try:
    response = requests.get(boxrec_url, headers = headers)

    # If the response was successful, no Exception will be raised
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
else:
    response.encoding = 'utf-8' # Optional: requests infers this internally
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('td', {'class': 'rowLabel'})
    print(links)