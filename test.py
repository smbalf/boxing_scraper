# RANDOM FILE FOR TESTING SCRIPTS

"""list = ['\n\n                    Gennadiy Golovkin\n    ', '  middle\n', '45', '\n        240\n      ', '2006-07-29\n', '40', 'orthodox', '5′ 10½″ \xa0 / \xa0 179cm', '70″ \xa0 / \xa0 178cm', 'Los Angeles, California, USA', ' Karaganda, Kazakhstan\n']


no_slash_n = [whitespace.replace('\n', '') for whitespace in list]
no_space = [whitespace.replace(' ', '') for whitespace in no_slash_n]

boxer_data = []

x = 0
for item in no_space:
    if x == 7 or x == 8:
        boxer_data.append(item[-5:-2])
    else:
        boxer_data.append(item)
    x+=1

"""

import csv

with open('boxrec_top_50_urls.csv', 'r') as top_50_urls_csv:
        reader = csv.reader(top_50_urls_csv)
        top_50_urls_list = []
        for row in reader:
            top_50_urls_list.append(', '.join(row))

        for url in top_50_urls_list:
            #print(url)
            boxrec_url = 'https://boxrec.com' + url
            print(boxrec_url)