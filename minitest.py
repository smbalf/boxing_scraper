# ANOTHER TEST FILE

target_list = ['name','division rating','division','bouts','rounds','KOs','debut','age','stance','height','reach','residence','birth place', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']

key_list = ['name','division rating','division','bouts','rounds','KOs','debut','height','reach','residence', 'wins', 'losses', 'draws', 'KO wins', 'KO losses']


for key in target_list:
    if key in key_list:
        pass
    else:
        key_list.insert(target_list.index(key), key)

print(key_list)