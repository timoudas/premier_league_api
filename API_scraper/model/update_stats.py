"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""
from directory import Directory 
import pandas as pd
from pprint import pprint

dirs = Directory()

def load_player_stats(start_year, end_year=None):
    """Load player_stats json files into a container
        Args:
            start_year(int): year of player_stats json
            end_year(int): year of player_stats json
    """
    if end_year == None:
        file = f'EN_PR_{start_year}_playerstats.json'
        stats_file = dirs.load_json(file, '..', 'json', 'params', 'stats')
        return stats_file
    else:
        all_files = [f'EN_PR_{year}_playerstats.json' for year in range(start_year,end_year+1)]
        container = []
        for file in all_files:
            stats_file = dirs.load_json(file, '..', 'json', 'params', 'stats')
            container.append(stats_file)
        return container
    
data = load_player_stats(2017)

for d in data:
    print(d)

