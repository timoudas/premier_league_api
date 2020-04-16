"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""
from directory import Directory 
import pandas as pd
from pprint import pprint
from functools import reduce 


dirs = Directory()

def deep_get(dictionary, keys, default=None):
    """Get values of nested keys from dict
        Args:
            dictionary(dict): Dict with nested keys
            keys(dict.keys()): "." separated chain of nested keys, ex "info.player.name"
    """
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

def load_player_stats(year):
    """Load player_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    file = f'EN_PR_{start_year}_playerstats.json'
    stats_file = dirs.load_json(file, '..', 'json', 'params', 'stats')
    stats_file.append({'season':start_year})
    return stats_file

"""Read stats from ...playerstats.json into Dataframe,
can later be used to import data into DataBase
"""

def read_playerstats(data):
    """Read stats from ...playerstats.json into flattened
    list of dicts. 
    """
    stats_all = []
    stats_temp = {}
    for d in data:
        stats_temp = {}
        if 'stats' in d:
            stats = d['stats']
            for dicts in stats:
                stats_temp['id'] = dicts.get('id')
                if dicts.get('name') != None:
                    stats_temp[dicts.get('name')] = dicts.get('value')
            stats_all.append(stats_temp)
    return stats_all

def read_playerinfo(data):
    """Read info from ...playerstats.json into flattened
    list of dicts. 
    """
    info_all = []
    for d in data:
        stats_temp = {}
        try:
            if 'info' in d:
                stats = d['info']
                stats_temp['age'] = stats.get('age')
                stats_temp['id'] = stats.get('id')
                stats_temp['birth'] = deep_get(stats, 'birth.date.label')
                stats_temp['birth_exact'] = deep_get(stats, 'birth.date.millis')
                stats_temp['country'] = deep_get(stats, 'birth.country.country')
                stats_temp['isoCode'] = deep_get(stats, 'birth.country.isoCode')
                stats_temp['loan'] = deep_get(stats, 'info.loan')
                stats_temp['position'] = deep_get(stats, 'info.position')
                stats_temp['positionInfo'] = deep_get(stats, 'info.positionInfo')
                stats_temp['shirtNum'] = deep_get(stats, 'info.shirtNum')
                stats_temp['name'] = deep_get(stats, 'name.display')
                stats_temp['first'] = deep_get(stats, 'name.first')
                stats_temp['last'] = deep_get(stats, 'name.last')
                stats_temp['nationalTeam'] = deep_get(stats, 'nationalTeam.country')
                stats_temp['playerId'] = stats.get('playerId')
            stats_temp['season'] = d.get('season')
            info_all.append(stats_temp)
        except Exception as e:
            print(e)

    return info_all

                
            
start_year = 2017
end_year = 2020
data = []
data_sample = load_player_stats(start_year)
stats = read_playerstats(data_sample)
info = read_playerinfo(data_sample)
df1 = pd.DataFrame(stats).set_index('id')
df2 = pd.DataFrame(info).set_index('id')
print(df1.head())
print(df2.head())








