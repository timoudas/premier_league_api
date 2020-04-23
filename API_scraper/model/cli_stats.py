#!/usr/bin/python

import sys
import os
import pickle
import argparse
import click
from directory import Directory
from directory import StorageConfig
from get_stats import SeasonStats



dir = Directory()

class CLIStats:

    def __init__(self):
        self.header = self.header()
        self.description = self.description()
        self.commands = self.commands()
        self.leagues = dir.load_json('season_params.json', StorageConfig.PARAMS_DIR)
        with open('league_seasons_init', 'rb') as f:
            self.pickle = pickle.load(f)

    @staticmethod
    def header():
        os.system('clear')
        print('\t','*'*60)
        print("\t\t***  Welcome - Football Stats generator  ***")
        print('\t','*'*60)

    @staticmethod
    def description():
        print('Interface to download: \t playerstats \t fixturestats \t team standing \n')
        print('Type "exit" to terminate shell')

    @staticmethod
    def commands():
        commands = {'View Leagues': '-v',
                    'View League Seasons': '-v LEAGUE',
                    'Download stats': '-d LEAGUE SEASON TYPE',
                    'Help' : '-h',}
        for key, value in commands.items():
            print("{: <25} {}".format(key, value))
        print('\n')

    def view_leagues(self):
        for league in self.leagues.keys():
            print("{: <10}".format(league), end="")
        print('\n')

    def view_seasons(self, league):
        if league in self.leagues:
            seasons = self.leagues[league]
            print(league,'seasons:')
            for season in seasons:
                print("{: <20}".format(season), end="")
            print('\n')
        else:
            print(league, 'is not avalible')
            print('\n')

    def download_stats(self, league, season, stat_type):
        league = league.upper()
        season_end = str(int(season)+1)
        season = str(season + '/' + season_end)
        stats = {'-p': 'player_stats',
                '-t': 'team_standings',
                '-f': 'fixture_stats'}
        if not stats.get(stat_type):
            print('Select a valid stats type: \t -p [Player] \t -f [Fixture] \t -t [Team]')
        else:
            if stats.get(stat_type) == 'player_stats':
                self.pickle[league + '_' + season].player_stats()
            elif stats.get(stat_type) == 'fixture_stats':
                self.pickle[league + '_' + season].fixture_stats()
            else:
                self.pickle[league + '_' + season].team_standings()



def main():
    interface = CLIStats()
    cmd = {'-v': interface.view_leagues,
           'exit': sys.exit,
           'View Stats Type': '-s',
           '-h' : 'interface.help', }
    while True:
        usr_command = input('CLIStats$ ')
        if usr_command in cmd.keys():
            cmd.get(usr_command)()
        elif len(usr_command.split(' ')) == 2:
            league = usr_command.split(' ')[-1]
            interface.view_seasons(league)
        elif len(usr_command.split(' ')) == 4:
            league = usr_command.split(' ')[1]
            season = usr_command.split(' ')[2]
            stat_type = usr_command.split(' ')[3]
            interface.download_stats(league, season, stat_type)
        else:
            print('Command not valid')
        #     print(usr_command)
        #     cmd[usr_command]





if __name__ == '__main__':
    main()




