#!/usr/bin/python
"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""
from directory import Directory
from directory import StorageConfig 
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
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def read_fixtureinfo(data):
    info_all = []
    try:
        for d in data:
            stats_temp = {}
            if 'info' in d:
                stats = d['info']
                stats_temp = \
                    {'gameweek_id' : deep_get(stats, 'gameweek.id'),
                    'season_label' : deep_get(stats, 'gameweek.compSeason.label'),
                    'id' : stats['id'],

                    'competition' : deep_get(stats, 'gameweek.compSeason.competition.description'),
                    'competition_abbr' : deep_get(stats, 'gameweek.compSeason.competition.abbreviation'),
                    'competition_id' : deep_get(stats, 'gameweek.compSeason.competition.id'),

                    'gameweek' : deep_get(stats, 'gameweek.gameweek'),
                    'kickoff' : deep_get(stats, 'kickoff.label'),
                    'kickoff_millis' : deep_get(stats, 'kickoff.millis'),

                    'home_team' : stats['teams'][0]['team']['name'],
                    'home_team_id' : stats['teams'][0]['team']['club']['id'],
                    'home_team_shortName' : stats['teams'][0]['team']['shortName'],
                    'home_team_score' : stats['teams'][0]['score'],

                    'away_team' : stats['teams'][1]['team']['name'],
                    'away_team_id' : stats['teams'][1]['team']['club']['id'],
                    'away_team_shortName' : stats['teams'][1]['team']['shortName'],
                    'away_team_score' : stats['teams'][1]['score'],

                    'ground' : deep_get(stats, 'ground.name'),
                    'grounds_id' : deep_get(stats, 'ground.id'),

                    'city' : deep_get(stats, 'ground.city'),
                    'fixtureType' : stats.get('fixtureType'),
                    'extraTime' : stats.get('extraTime'),
                    'shootout' : stats.get('shootout'),
                    'fixture_id' : stats.get('id'),

                    'clock_label' : deep_get(stats, 'clock.label'),
                    'clock_secs' : deep_get(stats, 'clock.secs'),}
                info_all.append(stats_temp)
    except TypeError as e:
        print("Check that data exists and is loaded correctly")
    return info_all

def read_fixturestats(data):
    """In key "stats" followed by teamID followed by key "M"

    """
    try:
        stats_all = []
        for d in data:
            stats_temp = {}
            stats_home = {}
            stats_away = {}
            if 'stats' in d:
                stats = d['stats']
                info = d['info']

                home_id_key = str(info['teams'][0]['team']['club']['id'])
                away_id_key = str(info['teams'][1]['team']['club']['id'])


                if away_id_key in stats:
                    if home_id_key in stats:
                        away = stats[away_id_key]['M']
                        home = stats[home_id_key]['M']
                        stats_away = {'away_' + stats.get('name'): stats.get('value') for stats in away}
                        stats_home = {'home_' + stats.get('name'): stats.get('value') for stats in home}
                        stats_temp.update(stats_away)
                        stats_temp.update(stats_home)
                        stats_temp.update({'id' : info['id']})

                stats_all.append(stats_temp)
        return stats_all
    except TypeError as e:
        print(e, "Check that data exists and is loaded correctly")

if __name__ == '__main__':
    pprint(read_fixturestats(load_fixture_stats(2019)))
  
