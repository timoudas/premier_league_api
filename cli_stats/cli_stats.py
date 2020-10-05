#!/usr/bin/env python
"""
Interactive command line interface to view avalible leagues and their seasons.
And download stats for a league
Usage:
    CLIStats$ (-i | --interactive)
    CLIStats$ view [LEAGUE]
    CLIStats$ clean [options] <LEAGUE> <SEASON>
Options:
    -i, --interactive    Interactive Mode
    -p,  --player         Playerstats
    -t,  --team           Team standings
    -f,  --fixture        Fixturestats
    -u,  --update         Update
"""
"""
Interactive Command Line for the following tasks:
    * View Leagues and their Seasons
    * Download Player/Team/Fixture stats for a League and Season
    * Clean downloaded data
    * Insert data in database
"""
import cmd
import datetime
import os
import sys

from docopt import DocoptExit
from docopt import docopt
from pprint import pprint

import clean_stats.clean_stats as clean

from database import mongo_db as db

from directory import Directory
from get_data.get_stats import SeasonStats
from storage_config import StorageConfig


dir = Directory()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class StatShell(cmd.Cmd):

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

    def __init__(self):
        super(StatShell, self).__init__()
        self.leagues = dir.load_json('season_params.json', StorageConfig.PARAMS_DIR)
        self.db_clean_params = [param for param in self.LOADING_CHOICES.keys()]


    os.system('clear')
    intro = '\n'.join([
        "\t" + "*"*60,
        "\t\t***  Welcome - Football Stats generator  ***",
        "\t" + "*"*60,
        "",
        "\tType help or ? to list commands,",
        "\t\tor help command to get help about a command."
    ])
    prompt = '(CLIStats$) '

    @docopt_cmd
    def do_view(self, arg):
        """Usage: CLIStats$ [LEAGUE] """
        if arg['LEAGUE']:
            league = arg['LEAGUE'].upper()
            if league in self.leagues:
                seasons = self.leagues[league]['label']
                show_league = self.leagues[league]['league_name']
                print(show_league,'seasons:')
                for season in seasons:
                    print("{: <20}".format(season), end="")
                print('\n')
            else:
                print(league, 'is not avalible')
                print('\n')
        else:
            for league in self.leagues.keys():
                print("{: <10}".format(league), end="")
            print('\n')

    def downloads_choices(self, type_stats, league, season):
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


    @docopt_cmd
    def do_download(self, arg):
        """Usage: CLIStats$ [options] <LEAGUE> <SEASON> ...

        Options:
                -p,  --player          Playerstats
                -t,  --team            TeamStandings
                -f,  --fixture         FixtureStats
                -s,  --squad           Squads
                -l,  --league          LeagueStandings
                -i,  --fixtureinfo     FixtureInfo
                -e,  --fixtureplayer   PlayerStats for Fixture
                """

        league = arg['<LEAGUE>'].upper()
        if len(arg['<SEASON>']) == 1:
            season_end = str(int(arg['<SEASON>'][0])+1)
            season = str(arg['<SEASON>'][0] + '/' + season_end)
            for key, value in arg.items():
                if value == True:
                    self.downloads_choices(key, league, season)
        else:
            for season in range(int(arg['<SEASON>'][0]), int(arg['<SEASON>'][-1])+1):
                start_season = str(int(season))
                end_season = str(int(season)+1)
                temp_season = f'{start_season}/{end_season}'
                for key, value in arg.items():
                    if value == True:
                        self.downloads_choices(key, league, temp_season)


    def loading_choices(self, type_stats, league, season):
        choices = {'-p': clean.playerstats,
                   '-t': clean.team_standings,
                   '-f': clean.fixturestats,
                   '-l': clean.league_standings,
                   '-e': clean.fixture_player_stats}
        if type_stats in choices.keys():
            return choices.get(type_stats)(league, season)

    @docopt_cmd
    def do_clean(self, arg):
        """Usage: CLIStats$ [options] <LEAGUE> <SEASON>

        Options:
            -p,  --player         Playerstats
            -t,  --team           Team standings
            -f,  --fixture        Fixturestats
            -l,  --league         League Standings
            -e   --player_fixture Player Fixture Stats
            """
        file_prefix = f"{arg['<LEAGUE>'].upper()}_{arg['<SEASON>']}_"
        league = arg['<LEAGUE>'].upper()
        season = str(arg['<SEASON>'])
        for key, value in arg.items():
            try:
                if value == True:
                    file_suffix = self.FILE_NAMES.get(key)
                    file_name = f'{file_prefix}{file_suffix}'
                    dir.save_json(file_name, self.loading_choices(key, league, season), StorageConfig.DB_DIR)
                    print(f'{file_name} was saved')
            except FileExistsError:
                print("Please check that", file_prefix, " exists")

    def push_choices(self, type_stats, database):
        choices = {'-p': db.executePushPlayer,
                   '-t': db.executePushTeam,
                   '-f': db.executePushFixture,
                   '-l': db.executePushLeagueStandings,
                   '-e': db.executePushFixturePlayerStats}
        if type_stats in choices.keys():
            return choices.get(type_stats)(database)

    @docopt_cmd
    def do_db(self, arg):
        """Usage: CLIStats$ [options] <LEAGUE> <SEASON>
        
        Options:
            -p,  --player         Push Playerstats
            -t,  --team           Push Team standings
            -f,  --fixture        Push Fixturestats
            -l,  --league         Push League Standings
            -e,  --player_fixture Push Player Fixture Stats
            """
        database = db.DB(arg['<LEAGUE>'].upper(), arg['<SEASON>'])
        for key, value in arg.items():
            if value == True:
                print("Pushing: ", arg['<LEAGUE>'].upper(), arg['<SEASON>'])
                self.push_choices(key, database)
        print("Push completed")

    @docopt_cmd
    def do_weekly(self, arg):
        """Usage: CLIStats$ (LEAGUE) (SEASON)"""
        #Download all files
        download_params = ['-p', '-t', '-f', '-s', '-l', '-i', '-e']
        if not len(arg['SEASON']) == 4:
            print('Season should be YYYY')
        else:
            database = db.DB(arg['LEAGUE'].upper(), arg['SEASON'])
            league = arg['LEAGUE'].upper()
            season_end = str(int(arg['SEASON'])+1)
            season = f"{arg['SEASON']}/{season_end}"
            file_season = str(arg['SEASON'])
            file_prefix = f"{arg['LEAGUE'].upper()}_{arg['SEASON']}_"

            for i in download_params:
                print("Downloading: ", i)
                self.downloads_choices(i, league, season)

            for arg_key in self.db_clean_params:
                file_suffix = self.FILE_NAMES.get(arg_key)
                file_name = f'{file_prefix}{file_suffix}'
                dir.save_json(file_name, self.loading_choices(key, league, season), StorageConfig.DB_DIR)
                print(f'{file_name} was saved')
            for arg_key in self.db_clean_params:
                self.push_choices(arg_key, database)

    @docopt_cmd
    def do_update(self, arg):
        """Usage: CLIStats$ [options] <LEAGUE>
        
        Options:
            -p,  --player         Push Playerstats
            -t,  --team           Push Team standings
            -f,  --fixture        Push Fixturestats
            -l,  --league         Push League Standings
            -e,  --player_fixture Push Player Fixture Stats
            """
        season = str(datetime.date.today().year)
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


    def do_clear(self, arg):
        """Clear the screen"""
        os.system('clear')
        print(self.intro)

    def do_exit(self, arg):
        """Exit the interpreter."""
        print("exiting ...")
        return True

def main():
    opt = docopt(__doc__, sys.argv[1:])

    if opt['--interactive']:
        StatShell().cmdloop()
    elif opt['--update']:
        print(opt)
        StatShell().do_update()

if __name__ == '__main__':
    main()
