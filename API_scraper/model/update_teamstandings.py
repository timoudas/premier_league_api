#!/usr/bin/python

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

def load_team_standings(year):
    """Load player_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'EN_PR_{year}_teamstandings.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")


def read_team_standings_stats(data):
    info_all = []
    # try:
    for d in data:
        stats_temp = {}
        if 'standing' in d:
            stats_all = d['standing']
            for stats in stats_all:
                if 'fixtures' in stats:
                    comp = stats['fixtures'][0]
                    stats_temp = \
                        {'played' : stats['played'],
                        'points' : stats['points'],
                        'position' : stats['position'],

                        'competition' : deep_get(comp, 'gameweek.compSeason.competition.description'),
                        'competition_abbr' : deep_get(comp, 'gameweek.compSeason.competition.abbreviation'),
                        'competition_id' : deep_get(comp, 'gameweek.compSeason.competition.id'),

                        'gameweek' : deep_get(comp, 'gameweek.gameweek'),
                        'kickoff' : deep_get(comp, 'kickoff.label'),
                        'kickoff_millis' : deep_get(comp, 'kickoff.millis'),

                        'home_team' : comp['teams'][0]['team']['name'],
                        'home_team_id' : comp['teams'][0]['team']['club']['id'],
                        'home_team_shortName' : comp['teams'][0]['team']['shortName'],
                        'home_team_score' : comp['teams'][0]['score'],

                        'away_team' : comp['teams'][1]['team']['name'],
                        'away_team_id' : comp['teams'][1]['team']['club']['id'],
                        'away_team_shortName' : comp['teams'][1]['team']['shortName'],
                        'away_team_score' : comp['teams'][1]['score'],
                        'ground' : comp['ground']['name'],
                        'grounds_id' : comp['ground']['id'],

                        'city' : comp['ground']['city'],
                        'fixtureType' : comp['fixtureType'],
                        'extraTime' : comp['extraTime'],
                        'shootout' : comp['shootout'],
                        'fixture_id' : comp['id'],

                        'clock_label' : comp['clock']['label'],
                        'clock_secs' : comp['clock']['secs'],}
                    
                info_all.append(stats_temp)
    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
    return info_all

def read_team_standings_info(data):
    """In key "stats" followed by teamID followed by key "M"

    """
    try:
        stats_all = []
        for d in data:
            season_temp = {}
            if 'season' in d:
                season_info = d['season']
                season_team = d['team']
                season_temp = \
                {'league_season': season_info['label'],
                 'competition_abbr': season_info['abbreviation'],
                 'competition' :  season_info['description'],
                 'competition_id' : d['id'],
                 'team_name' : season_team['name'],
                 'team_id' : deep_get(season_team, 'club.id'),
                 'team_shortName': deep_get(season_team, 'club.shortName'),
                }


        return stats_all
    except TypeError as e:
        print("Check that data exists and is loaded correctly")

if __name__ == '__main__':
    pprint(read_team_standings_stats(load_team_standings(2019)))