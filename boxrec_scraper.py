from bs4 import BeautifulSoup
import re
import csv
from scrapingbee import ScrapingBeeClient



# Creating lists to store data on boxers
# key_list has some hard coded values as these require alternative methods to scrape the corresponding data
key_list = ['name', 'division rating', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
dirty_value_list = []
clean_value_list = []
# Creating the CSV column headers and dict to store key-value pair
csv_headers = ['name', 'division rating', 'division', 'bouts', 'rounds', 'KOs', 'debut', 'age', 'stance', 'height', 'reach', 'residence', 'birth place', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
csv_dict = {}


def rotate_boxer_urls():
    """
    Function uses the scrapingbee library to evade bans on boxrec.com, API is stored on a txt file and gitignored.
    boxrec_urls.py was used to obtain the boxrec URLs of the top 50 boxers in each weight category (16), totalling 800.
    NOTE: Boxrec updates boxer's ratings actively and so it might be more accurate to timestamp the data (19/10/2022).

    rotate_boxer_urls gets a BeautifulSoup response of the url before calling grab_boxer_data(response)
    The data obtained from the page is then cleaned via clean_lists() and clean_dict()
    Lastly the data which with a correctly corresponding KEY in the dictionairy is appended to a CSV file
    with write_to_csv()
    The rotate_boxer_url then continues to loop through each URL in the boxrec_top_50_urls until complete.
    """
    global key_list
    global dirty_value_list
    global clean_value_list

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

            grab_boxer_data(bs)
            
            clean_lists(dirty_value_list, clean_value_list)
            
            clean_dict(csv_dict)

            write_to_csv(csv_headers, csv_dict)
            
            # Reseting list values
            key_list = ['name', 'division rating', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
            dirty_value_list = []
            clean_value_list = []
            
            # Below check to see which url was scraped before moving to the next url
            print(boxrec_url)
            print('---------------------------------------------')


def grab_boxer_data(soup):
    """
    Gathers the required data from a boxer's boxrec profile page.
    Access variable describes whether the response was successful, if not closes the script.
    Due to the the profile page design, items have to be individually searched for in many cases.
    Name, rating, wins/losses/draws/ko wins/ ko losses, all require searching for individually.
    Reach is also individually obtained as it doesn't match the same structure as similar elements on the page 
    The remaining values can be programmatically obtained for key-value pairs.
    """
    boxrec_tables = soup.find_all('td', {'class': 'rowLabel'})
    access = len(boxrec_tables)

    if access == 0:
        print('7.. 8.. 9.. 10! BOXREC KO!')
        print('Closing scripts...')
        exit()
    else:
        print(f'SCRAPING...')

    boxer_name = soup.find('h1').get_text()
    dirty_value_list.append(boxer_name)

    ratings = []
    for link in soup.find_all('a', href=re.compile('^(/en/ratings?)')):
        ratings.append(link.get_text())

    try:
        no_slash_n = [whitespace.replace('\n', '') for whitespace in ratings]
        no_space = [whitespace.replace(' ', '') for whitespace in no_slash_n]
        rating = no_space[1]
        division_rating = rating[1:3]
        dirty_value_list.append(division_rating)
    
    # Some boxers in the Top 50 can suddenly become "inactive" and hence have their rating removed
    # This is a catch for that
    except Exception:
        dirty_value_list.append('')

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

    # Obtain key-value pairs for boxer data
    for table_value in boxrec_tables:
        first_td = table_value.find_all('b')
        for item in first_td:
            key = item.get_text()
            value = item.find_next().get_text()
            key_list.append(key)
            dirty_value_list.append(value)
            
            # Obtain data on boxers reach if it exists
            if item.get_text() == 'reach':
                value_reach = item.find_next().find_next().find_next()
                boxer_reach = value_reach.get_text()
                key_list.append(key)
                dirty_value_list.append(boxer_reach)


def clean_lists(dirty_list, clean_list):
    """
    Initial cleaning of the raw data from the scraping
    Target list matches the intended CSV headers
    Not all boxers will have the data on their page and so if the key doesn't exist, we create it,
    before inserting an empty '' value to the corresponding index in the values list.
    """
    global csv_headers
    global csv_dict

    print('CLEANING THE DATA...')
    # Cleans the data removing unwanted string values
    no_pct = [pct.replace('%', '') for pct in dirty_list]
    no_slash_n = [whitespace.replace('\n', '') for whitespace in no_pct]
    no_fwd_slash = [fwd_slash.replace('/', '') for fwd_slash in no_slash_n]
    no_space = [whitespace.replace(' ', '') for whitespace in no_fwd_slash]
    no_xa0 = [xa0.replace('\xa0', '') for xa0 in no_space]
    no_comma = [comma.replace(',', ' ') for comma in no_xa0]
    for value in no_comma:
        clean_list.append(value)

    target_list = ['name','division rating','division','bouts','rounds','KOs','debut','age','stance','height','reach','residence','birth place', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']
      
    for key in target_list:
        if key in key_list:
            pass
        else:
            key_list.insert(target_list.index(key), key)
            clean_list.insert(target_list.index(key), '')
    # Creates a dictionary with the key list and cleaned values 
    # This is all the data before selecting those that we want to send to the CSV
    boxer_dict = dict(zip(key_list, clean_value_list))

    # Takes only those values for the CSV as per csv_headers
    csv_values = [boxer_dict[header] for header in csv_headers]
    # Creates final dictionary ready for writing to the CSV
    csv_dict = dict(zip(csv_headers, csv_values))
    print('CREATED CSV DICTIONARY')
    

def clean_dict(csv_dict=csv_dict):
    """
    Cleans the values for respective keys.
    Perhaps need a specific fix instead of replacing all missing values with "NO DATA"
    This has caused an issue where columns filled with integers or dates get typed as strings
    """
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
            csv_dict[item] = 'None'

    print('DATA CLEANED, READY FOR CSV')


def write_to_csv(csv_header=csv_headers, csv_dict=csv_dict):
    """Simply appends the data to the boxrec_tables.csv file"""
    with open('boxrec_tables.csv', 'a', encoding="utf-8", newline='') as boxrec_csv:
        writer = csv.DictWriter(boxrec_csv, fieldnames=csv_headers)
        print('WRITING TO CSV...')
        writer.writerow(csv_dict)


# Run the script!
rotate_boxer_urls()
