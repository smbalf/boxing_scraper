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

print(bout_data_dict['url']['bout_info']['bout_result'])

bout_data_dict['url']['bout_info']['bout_result'] = 5

print(bout_data_dict['url']['bout_info']['bout_result'])