"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""
from directory import Directory 
from directory import Storageconfig 
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
    try: 
        file = f'EN_PR_{year}_playerstats.json'
        stats_file = dirs.load_json(file, Storageconfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def read_playerstats(data):
    """Read stats from ...playerstats.json into flattened
    list of dicts. 
    """
    try:
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
    except TypeError as e:
        print("Check that data exists and is loaded correctly")

def read_playerinfo(data):
    """Read info from ...playerstats.json into flattened
    list of dicts. 
    """
    info_all = []
    # try:
    for d in data:
        stats_temp = {}
        if 'info' in d:
            stats = d['info'] #Gets the info key in each dict
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
        stats_temp['season'] = data[-1]['season']
        info_all.append(stats_temp)

    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
    return info_all
              
def playerstats(start_year, end_year=None):
    """Data cleaning for playerstats"""
    try:
        if end_year == None:
            end_year = start_year
        df = pd.DataFrame()
        data = []
        for i in range(start_year, end_year):
            data_sample = load_player_stats(i)
            stats = read_playerstats(data_sample)
            info = read_playerinfo(data_sample)
            df1 = pd.DataFrame(stats)
            df2 = pd.DataFrame(info)
            df3 = pd.merge(df1, df2, on='id')
            df = df.append(df3)
    except Exception as e:
        print(e)
    return df


if __name__ == '__main__':
    pprint(read_playerinfo(load_player_stats(2018)))





