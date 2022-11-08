import requests
import re
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0'}
boxrec_url = 'https://boxrec.com/en/box-pro/15243'

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
        grab_table_data(soup, boxrec_url)


bout_data_dict = {
    'url': {
        'bout_date': 'date',
        'bout_info': {
            'opp_url': 'opp_url',
            'opp_name': 'opp_name',
            'opp_wins': 'opp_wins',
            'opp_losses': 'opp_losses',
            'opp_draws': 'opp_draws',
            'bout_result': 'bout_result',
            'round_ended': 'round_ended'  # WHY CANT I GET THIS???
        }
    }
}

def grab_table_data(soup, fighter_url):
    fighter_url = fighter_url
    bout_hist_table = soup.find_all('table', {'class': 'dataTable'})

    for table_value in bout_hist_table:

        date_text = table_value.find_all('a', href=re.compile('^(/en/date?)'))
        for dates in date_text:
            date = dates.get_text()
            
        a_tag_text = table_value.find_all('a', href=re.compile('^(/en/box-pro)'))
        for string in a_tag_text:
            grab_url = re.search('href="(.*)">', str(string))
            opp_url = grab_url.group(1)
            try:
                grab_name = re.search('>(.*)</a>', str(string))
                opp_name = grab_name.group(1)
            except AttributeError:
                opp_name = string.get_text()

        text_won = table_value.find_all('span', {'class': 'textWon'})
        for text in text_won:
            opp_wins = text.get_text()

        text_lost = table_value.find_all('span', {'class': 'textLost'})
        for text in text_lost:
            opp_losses = text.get_text()

        text_draw = table_value.find_all('span', {'class': 'textDraw'})
        for text in text_draw:
            opp_draws = text.get_text()

        text_debut = table_value.select('span[style="font-weight:bold;color:grey;"]')
        for text in text_debut:
            opp_debut = text.get_text()
        
        text_bout_result = table_value.select('div[class*="boutResult"]')
        for text in text_bout_result:
            bout_result = text.get_text()



        
        


launch_soup()
