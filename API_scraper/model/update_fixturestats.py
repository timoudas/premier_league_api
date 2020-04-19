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

def load_fixture_stats(year):
    """Load player_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'EN_PR_{year}_fixturestats.json'
        stats_file = dirs.load_json(file, '..', 'json', 'params', 'stats')
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def read_fixturestats(data):
    pass

def read_fixtureinfo(data):
    info_all = []
    try:
        for d in data:
            stats_temp = {}
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
                stats_temp['season'] = data[-1]['season']
                info_all.append(stats_temp)
    except TypeError as e:
        print("Check that data exists and is loaded correctly")
    return info_all
