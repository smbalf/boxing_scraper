from http.cookiejar import Cookie
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import csv
import boxrec_urls as bru
import time

pages = set()

def get_links(page_url):
    print("running scraper...")
    global pages
    for url in bru.url_list:
        req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        print(f'reading {url}')
        bs = BeautifulSoup(html.read(), 'html.parser')
        for link in bs.find_all('a', href=re.compile('^(/en/box-pro/)')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    new_page = link.attrs['href']
                    print(new_page)
                    pages.add(new_page)
                    time.sleep(2)

os.system('cls')

get_links('')

print("scraping done.")

print("now writing to csv...")

with open('boxrec_top_50_urls.csv', mode='a+', newline ='') as boxrec_file:
    boxrec_writer = csv.writer(boxrec_file, delimiter=',')
    for data in pages:
        boxrec_writer.writerows([[data]])

print("created csv.")








