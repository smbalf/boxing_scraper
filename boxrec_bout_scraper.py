import requests
import re
from bs4 import BeautifulSoup
import pprint
import csv
from scrapingbee import ScrapingBeeClient
import pandas as pd

def rotate_boxer_urls():
    # Obtaining API key
    with open('api_key.txt', 'r') as key_file:
        API_KEY = key_file.read()

    # Obtaining list of URLs to be scraped
    with open('boxrec_top_50_urls.csv', 'r') as top_50_urls_csv:
        reader = csv.reader(top_50_urls_csv)
        top_50_urls_list = []
        for row in reader:
            top_50_urls_list.append(', '.join(row))

    # Creating request to scrape each URL
    for url in top_50_urls_list:
        boxrec_url = 'https://boxrec.com' + url
        api_key = API_KEY
        PARAMS = {"render_js": 'False'}

        client = ScrapingBeeClient(api_key=api_key)

        # Catching errors and printing
        try:
            response = client.get(boxrec_url, params=PARAMS )
            response.raise_for_status()
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response.encoding = 'utf-8'
            # Scrape the page!
            bs = BeautifulSoup(response.text, 'lxml')

            check_can_scrape(bs)

            # Below check to see which url was scraped before moving to the next url
            print(boxrec_url)
            print('---------------------------------------------')

def launch_soup():
    headers = {'User-Agent': 'Mozilla/5.0'}
    boxrec_url = 'https://boxrec.com/en/box-pro/15243'
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

def clean_name(name):
    no_pct = name.replace('%', '')
    no_slash_n = no_pct.replace('\n', '')
    no_fwd_slash = no_slash_n.replace('/', '')
    no_space = no_fwd_slash.replace(' ', '')
    no_xa0 = no_space.replace('\xa0', '')
    no_comma = no_xa0.replace(',', ' ')
    split_name = re.findall('[A-Z][a-z]+', no_comma)
    cleaned_name = ' '.join(split_name)
    return cleaned_name

boxer_name_list = []
def grab_table_data(soup):
    global boxer_name_list
    boxer_name = clean_name(soup.find('h1').get_text()) # GET BOXER NAME
    boxer_name_list.append(boxer_name)

    date_list = []
    opp_url_list = []
    opp_name_list = []
    opp_wins_list = []
    opp_losses_list = []
    opp_draws_list = []
    bout_result_list = []
    
    bout_hist_table = soup.find_all('table', {'class': 'dataTable'})
    for table_value in bout_hist_table:
        date_text = table_value.find_all('a', href=re.compile('^(/en/date?)'))
        for dates in date_text:
            date = dates.get_text() # GET ALL BOUT DATES
            date_list.append(date)

        a_tag_text = table_value.find_all('a', href=re.compile('^(/en/box-pro)'))
        for string in a_tag_text:
            grab_url = re.search('href="(.*)">', str(string))
            opp_url = grab_url.group(1) # GET OPPONENT BOXREC URL
            opp_url_list.append(opp_url)
            try:
                grab_name = re.search('>(.*)</a>', str(string))
                dirty_opp_name = grab_name.group(1)  # GET OPPONENT NAME
                opp_name = clean_name(dirty_opp_name)
                opp_name_list.append(opp_name)
            except AttributeError:
                dirty_opp_name = string.get_text() # GET OPPONENT NAME
                opp_name = clean_name(dirty_opp_name)
                opp_name_list.append(opp_name)

        text_won = table_value.find_all('span', {'class': 'textWon'})
        for text in text_won:
            opp_wins = text.get_text() # GET OPPONENT WINS
            opp_wins_list.append(opp_wins)

        text_lost = table_value.find_all('span', {'class': 'textLost'})
        for text in text_lost:
            opp_losses = text.get_text() # GET OPPONENT LOSSES
            opp_losses_list.append(opp_losses)

        text_draw = table_value.find_all('span', {'class': 'textDraw'})
        for text in text_draw:
            opp_draws = text.get_text() # GET OPPONENT DRAWS
            opp_draws_list.append(opp_draws)

        text_debut = table_value.select('span[style="font-weight:bold;color:grey;"]')
        for text in text_debut:
            debut_text = text.get_text()
            if debut_text == 'debut': # DEBUT BOOLEAN CHECK AND SET
                opp_debut = True
            else:
                opp_debut = False

        text_bout_result = table_value.select('div[class*="boutResult"]')
        for text in text_bout_result:
            bout_result = text.get_text() # GET BOUT RESULT
            bout_result_list.append(bout_result)

    number_of_bouts = list(range(len(date_text), 0, -1)) # GET NUMBER OF BOUTS FOUGHT BY BOXER BEING SCRAPED

    zipped_data = zip(number_of_bouts, date_list, opp_url_list, opp_name_list, opp_wins_list, opp_losses_list, opp_draws_list, bout_result_list)
    boxrec_dict(boxer_name, zipped_data)


bout_data_dict_list = []
def boxrec_dict(name, zipped_data):
    global bout_data_dict_list
    bout_data_dict = {
        name: ({ 
            bn: {'bout_date': bd, 'opp_url': ou, 'opp_name': on, 'opp_wins': ow, 'opp_losses': ol, 'opp_draws': od, 'bout_result': br} 
            for bn, bd, ou, on, ow, ol, od, br in zipped_data
            })
    }

    bout_data_dict_list.append(bout_data_dict)
    #print(bout_data_dict_list)

    #print('writing to csv')
    #write_to_csv(bout_data_dict_list)
    create_merged_dict(bout_data_dict_list, final_dict)

final_dict = {}

def create_merged_dict(bout_list, main_dict):
    for boxer_dict in bout_list:
        main_dict = {**main_dict, **boxer_dict}

    create_dict_DF(main_dict)
    

def create_dict_DF(main_dict):
    x = pd.DataFrame.from_dict({(i,j): main_dict[i][j] 
                            for i in main_dict.keys() 
                            for j in main_dict[i].keys()},
                        orient='index')

    x.to_csv('bout_data_two.csv', encoding='utf-8', mode='w', header=False, index=True,)


def write_to_csv(list_of_dict):
  with open('bout_data.csv','w', encoding="utf-8", newline='') as bout_data_csv:
    writer = csv.DictWriter(bout_data_csv, fieldnames=boxer_name_list)
    writer.writeheader()
    writer.writerows(list_of_dict)


# RUNNING THE SCRIPT
rotate_boxer_urls() # PROXY
# launch_soup()   # NO PROXY