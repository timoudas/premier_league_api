"""Python sub-proccesses for use in node.js to fetch/clean/push data
to database

Usage:
  subprocess_cli.py -u [options] <LEAGUE>

Options:
  -p  --player              Update PlayerStats.
  -t  --team                Update TeamStandings.
  -f  --fixture             Update FixtureStats.
  -l  --leauge              Update LeagueStandings.
  -e  --playerfixture       Update PlayerFixture.
"""


import cmd
import datetime
import os
import sys


from docopt import docopt
from pprint import pprint

import clean_stats.clean_stats as clean

from database import mongo_db as db

from directory import Directory
from get_data.get_stats import SeasonStats
from storage_config import StorageConfig

SEASON = str(datetime.date.today().year)
dir = Directory()

LOADING_CHOICES = {
    '-p': clean.playerstats,
    '-t': clean.team_standings,
    '-f': clean.fixturestats,
    '-l': clean.league_standings,
    '-e': clean.fixture_player_stats,
}

FILE_NAMES = {
    '-p':'playerstats',
    '-t': 'team_standings',
    '-f': 'fixturestats',
    '-l': 'league_standings',
    '-e': 'player_fixture'
}

def downloads_choices(type_stats, league, season):
    """Returns an instance of a class that runs a download function
        Args:
            type_stats (str): One of below keys in the dict
            league (str): A league abbreviation, ex. EN_PR
            season (str): A valid season, ex 2019/2020
    """
    stats = SeasonStats()
    choices = {'-p': ['player_stats', league, season],
               '-t': ['team_standings', league, season],
               '-f': ['fixture_stats', league, season],
               '-s': ['team_squad', league, season],
               '-l': ['league_standings', league, season],
               '-i': ['fixture_info', league, season],
               '-e': ['fixture_player_stats', league, season]}
    params = choices.get(type_stats)
    return stats(*params)

def loading_choices(type_stats, league, season):
    choices = {'-p': clean.playerstats,
               '-t': clean.team_standings,
               '-f': clean.fixturestats,
               '-l': clean.league_standings,
               '-e': clean.fixture_player_stats}
    if type_stats in choices.keys():
        return choices.get(type_stats)(league, season)

def push_choices(type_stats, database):
    choices = {'-p': db.executePushPlayer,
               '-t': db.executePushTeam,
               '-f': db.executePushFixture,
               '-l': db.executePushLeagueStandings,
               '-e': db.executePushFixturePlayerStats}
    if type_stats in choices.keys():
        return choices.get(type_stats)(database)

def create_file_name(league, key):
    file_prefix = f"{league}_{SEASON}_"
    file_suffix = FILE_NAMES.get(key)
    file_name = f'{file_prefix}{file_suffix}'
    return file_name

def update_league_standings(league, key):
    database = db.DB(league, SEASON)
    file_name = create_file_name(league, ket)
    downloads_choices(key, league, SEASON)
    dir.save_json(file_name, loading_choices(key, league, SEASON), StorageConfig.DB_DIR)
    push_choices(key, database)

def update_player_stats(league):
    pass

def update_fixture_stats(league):
    pass

def update_team_standings(league):
    pass

def update_fixture_player_stats(league):
    pass


def dispatch(type_stats, league):
    choices = {'-p': update_player_stats,
               '-t': update_team_standings,
               '-f': update_fixture_stats,
               '-l': update_league_standings,
               '-e': update_fixture_player_stats}
    if type_stats in choices.keys():
        return choices.get(type_stats)(league, type_stats)

def update(self):

    
    league = arg['<LEAGUE>'].upper()
    database = db.DB(league, season)
    print('working')
    for key, value in arg.items():
        if value == True:
            if value == '-f':
                self.downloads_choices(key, league, season)
                self.downloads_choices('-i', league, season)
                file_prefix = f"{league}_{season}_"
                file_suffix_stats = self.FILE_NAMES.get(key)
                file_suffix_info = self.FILE_NAMES.get('-i')
                file_name_fix = f'{file_prefix}{file_suffix_stats}'
                file_name_info = f'{file_prefix}{file_suffix_info}'
                dir.save_json(file_name_fix, self.loading_choices(key, league, season), StorageConfig.DB_DIR)
                dir.save_json(file_name_info, self.loading_choices('-i', league, season), StorageConfig.DB_DIR)
            else:
                self.downloads_choices(key, league, season)
                file_prefix = f"{league}_{season}_"
                file_suffix = self.FILE_NAMES.get(key)
                file_name = f'{file_prefix}{file_suffix}'
                dir.save_json(file_name, self.loading_choices(key, league, season), StorageConfig.DB_DIR)
                self.push_choices(key, database)


if __name__ == '__main__':
    args = docopt(__doc__, version='Naval Fate 2.0')
    for key, value in args.items():
        if value == True:
            dispatch(key, args['<LEAGUE>'].upper())