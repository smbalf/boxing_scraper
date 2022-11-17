import pprint
import csv
import pandas as pd

dates = ['1-1', '2-1', '3-2', '4-2', '5-3', '6-4', '7-4']
# number_of_bouts = len(dates)
boxer_name = 'terry'
bout_no = ['7', '6', '5', '4', '3', '2', '1']
opp_name = ['sam', 'jim', 'jack', 'stuart', 'james', 'john', 'simon']
opp_wins = ['1', '2', '3', '4', '5', '6', '7']
opp_losses = ['1', '2', '3', '4', '5', '6', '7']
opp_draws = ['1', '2', '3', '4', '5', '6', '7']
opp_debut = [False, False, False, False, False, False, False]
opp_url = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg']
bout_result = ['w', 'w', 'w', 'w', 'l', 'w', 'w']

z = zip(bout_no, dates, opp_url, opp_name, opp_wins, opp_losses, opp_draws, opp_debut, bout_result)

bout_data_dict = {
    boxer_name: ({ 
        bn: {'bout_date': bd, 'opp_url': ou, 'opp_name': on, 'opp_wins': ow, 'opp_losses': ol, 'opp_draws': od, 'opp_debut': odb, 'bout_result': br} 
        for bn, bd, ou, on, ow, ol, od, odb, br in z
        })
    }
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(bout_data_dict)
names = ['terry']

bout_data_dict_list = []
bout_data_dict_list.append(bout_data_dict)


def write_to_csv(list_of_dict):
    print(list_of_dict)
    with open('bout_data.csv','w', encoding="utf-8", newline='') as bout_data_csv:
        writer = csv.DictWriter(bout_data_csv, fieldnames=names)
        writer.writeheader()
        writer.writerows(list_of_dict)
    
# write_to_csv(bout_data_dict_list)

b = {
    'Sam': {
        1: {
            'ab':3,
            'ba':9
        },
        2: {
            'ab':4,
            'ba':10
        }
    }
}

a = {
    'Inaki': {
        1: {
            'ab':2,
            'ba':4
        },
        2: {
            'ab':9,
            'ba':0
        }
    }
}

c = {
    'James': {
        1: {
            'ab':6,
            'ba':1
        },
        2: {
            'ab':7,
            'ba':8
        }
    }
}

g = {}

xx = [a, b, c]

def create_merged_dict(xx, main_dict):
    for boxer_dict in xx:
        main_dict = {**main_dict, **boxer_dict}

    create_dict_DF(main_dict)
    
    

def create_dict_DF(main_dict):
    x = pd.DataFrame.from_dict({(i,j): main_dict[i][j] 
                            for i in main_dict.keys() 
                            for j in main_dict[i].keys()},
                        orient='index')
    
    print(x)

# create_merged_dict(xx,g)


xxx = pd.read_csv('bout_data.csv',index_col=[0,1])

print(xxx)

