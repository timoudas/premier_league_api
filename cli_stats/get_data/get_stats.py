import json
import multiprocessing
import os
import re
import requests
import sys
import time
import uuid 

import datetime

from datetime import date



from .api_scraper.api_scraper import Football
from directory import Directory
from multiprocessing import Pool
from pprint import pprint
from storage_config import StorageConfig
from tqdm import tqdm



def load_match_data(url):
    """Retreives Ids for different pages on the API"""
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
              }
    params = (('pageSize', '100'),)
    # request to obtain the team info
    try:
        response = requests.get(url, params = params, headers=headers).json()
        data = response
        return data
    except Exception as e:
        print(e, 'Something went wrong with the request')
        return {}

class Base():
    fb = Football()
    dir = Directory()

    def __init__(self, league, season):
        """Initiates the class by counting the cores for later multiprocessing.

            Args:
                league(str): A league in the form of it's abbreviation. Ex. 'EN_PR'
                season(str): A season that exists for that specific league EX. '2019/2020'
        """
        self.pool = multiprocessing.cpu_count()
        self.league = league
        self.season = season
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        self.season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        self.teams = self.fb.leagues[self.league].seasons[self.season].load_teams()
        self.year = re.search( r'(\d{4})', self.season).group()



    def save_completed(self, filename, stats_list, path):
        """Saves dict to json file.

        Args:
            filename(str): The name of the file
            stats_list(list of dicts): The content that is to be saved
            path(str): The path to were the content is to be saved

        """
        year = self.year 
        filename = self.league + '_' + year + '_' + filename
        self.dir.save_json(filename, stats_list, path)
        print(f'Saved as {filename}.json in {path}')

class PlayerStats(Base):

    def __init__(self, *args, **kwargs):
        """Player IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.player_ids = self.load_season_players()
        self.player_dispatch_map = { 'player_stats' : self.player_stats}


    def load_season_players(self):
        """Loads the players for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} players')
        player_id = []
        for team in tqdm(self.teams.values()):
            try:
                players = self.fb.leagues[self.league].seasons[self.season].teams[team['shortName']].load_players()
            except:
                print(f"Found no players for {self.league} {self.season} {team}")
        if players:
            for player in players.keys():
                player_id.append(player)
        else:
            ('No players found..')
        print('Initialization completed')
        return player_id

    def player_stats_singel(self, player):
        """Gets stats for a player"""
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/stats/player/{player}?compSeasons={self.season_id}')
        return ds

    def player_stats(self):
        """Gets stats for all players in a league-season using multithreading
        saves output in a json file.
         """
        stats_list = []
        print("Getting player stats..")
        with Pool(self.pool) as p:
            player_stats = list(tqdm(p.imap(self.player_stats_singel, self.player_ids), total=len(self.player_ids)))
        print('Getting data from workers..')
        all_players = player_stats
        i = 0
        for player in all_players:
            stats = {"info": {}}
            stats["info"] = player['entity']
            stats['uuid'] = str(uuid.uuid4())
            if player['stats']:
                stats['stats'] = player['stats']
                stats['stats'].append({'id':player['entity']['id']})
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} players retreived had no stats')
        self.save_completed('playerstats', stats_list, StorageConfig.STATS_DIR)

class FixtureStats(Base):

    def __init__(self, *args, **kwargs):
        """Fixture IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.fixture_ids = [fix['id'] for fix in self.load_season_fixture().values()]
        self.fixture_dispatch_map = {'fixture_stats' : self.fixture_stats,
                             'fixture_info': self.fixture_info}

    def load_season_fixture(self):
        """Loads the fixtures for a league-season,
        calls api_scraper.py methods
        """

        print(f'Initializing \t {self.league} \t {self.season} fixtures')
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()

    def fixture_stats_singel(self, fixture):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
        return ds

    def fixture_stats(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats_list = []
        print("Getting fixture stats..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for fixture in fixture_stats:
            stats = {}
            stats['info'] = fixture['entity']
            stats['uuid'] = str(uuid.uuid4())
            if 'data' in fixture:
                stats['stats'] = fixture['data']
            else:
                i += 1
            if stats:
                stats_list.append(stats)

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('fixturestats', stats_list, StorageConfig.STATS_DIR)

    def fixture_info_singel(self, fixture_id):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/fixtures/{fixture_id}')
        return ds

    def fixture_info(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats_list = []
        print("Getting fixture info..")
        with Pool(self.pool) as p:
            fixture_info = list(tqdm(p.imap(self.fixture_info_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for info in fixture_info:
            stats = {}
            if info:
                stats = info
                stats['uuid'] = str(uuid.uuid4())
            else:
                i += 1
            if stats:
                stats_list.append(stats)

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('fixtureinfo', stats_list, StorageConfig.STATS_DIR)

class TeamStats(Base):

    def __init__(self, *args, **kwargs):
        """Team IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.team_ids = [team['id'] for team in self.load_season_teams().values()]
        self.team_dispatch_map = {'team_standings' : self.team_standings,
                             'team_squad': self.team_squad}


    def load_season_teams(self):
        """Loads the teams for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} teams')
        player_id = []
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_teams()

    def team_standings_singel(self, team_id):
        """Gets standing for a team"""
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/compseasons/{self.season_id}/standings/team/{team_id}')
        return ds

    def team_standings(self):
        """Gets standings for all teams in a league-season using multithreading
        saves output in a json file.
         """
        stats_list = []
        print("Getting team standings for: ", self.year)
        with Pool(self.pool) as p:
            team_standings = list(tqdm(p.imap(self.team_standings_singel, self.team_ids), total=len(self.team_ids)))
        print('Getting data from workers..')
        i = 0
        team_standing = team_standings
        for team in team_standing:
            stats = {"season": {}, "team": {}, "standing": {}}
            stats['uuid'] = str(uuid.uuid4())
            if 'compSeason' in team:
                stats['season'] = team['compSeason']
            if 'team' in team:
                stats['team'] = team['team']
            if 'entries' in team:
                stats['standing'] = team['entries']
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} teams retreived had no standings')
        self.save_completed('teamstandings', stats_list, StorageConfig.STATS_DIR)

    def team_squad_singel(self, team_id):
        """Gets stats for a player"""
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/teams/{team_id}/compseasons/{self.season_id}/staff')
        return ds

    def team_squad(self):
        """Gets standings for all teams in a league-season using multithreading
        saves output in a json file.
         """
        stats_list = []
        print("Getting team standings..")
        with Pool(self.pool) as p:
            team_squads = list(tqdm(p.imap(self.team_squad_singel, self.team_ids), total=len(self.team_ids)))
        print('Getting data from workers..')
        i = 0
        team_squad = team_squads
        for team in team_squad:
            stats = {"season": {}, "team": {}, "officials": {}}
            stats['uuid'] = str(uuid.uuid4())
            if 'compSeason' in team:
                stats['season'] = team['compSeason']
            if 'team' in team:
                stats['team'] = team['team']
            if 'players' in team:
                stats['players'] = team['players']
            if 'officials' in team:
                stats['officials'] = team['officials']
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} teams retreived had no standings')
        self.save_completed('teamsquads', stats_list, StorageConfig.STATS_DIR)

class LeagueStats(Base):

        def __init__(self, *args, **kwargs):
            Base.__init__(self, *args, **kwargs)
            self.league_dispatch_map = { 'league_standings' : self.league_standings}

        def league_standings(self):
            """Gets standing for a league"""
            response = load_match_data(
                f'https://footballapi.pulselive.com/football/standings?compSeasons={self.season_id}')
            stats_list = response['tables'][0]['entries']
            for d in stats_list:
                d['uuid'] = str(uuid.uuid4())
            print('Completed')
            self.save_completed('league_standings', stats_list, StorageConfig.STATS_DIR)

class SeasonStats(PlayerStats, TeamStats, FixtureStats, LeagueStats):

    def __init__(self, *args, **kwargs):
        """Empty construtor for lazy initiation of inherited
        sub-classes."""
        pass


    def __call__(self, called_method, *args, **kwargs):
        """Calls a method from a sub-class

            Args:
                called_method (str): Existing method in one of the sub-classes
                *args (str): League and Season
        """

        if hasattr(PlayerStats, called_method):
            PlayerStats.__init__(self, *args, **kwargs)
            self.player_dispatch_map.get(called_method)()

        elif hasattr(TeamStats, called_method):
            TeamStats.__init__(self, *args, **kwargs)
            self.team_dispatch_map.get(called_method)()

        elif hasattr(FixtureStats, called_method):
            FixtureStats.__init__(self, *args, **kwargs)
            self.fixture_dispatch_map.get(called_method)()

        elif hasattr(LeagueStats, called_method):
            LeagueStats.__init__(self, *args, **kwargs)
            self.league_dispatch_map.get(called_method)()
        else:
            raise(ValueError)

class SeasonStatsUpdate:
    dir = Directory()

    def __init__(self, league, season):
        self.today = date.today().strftime("%s")
        self.league = league
        self.season = season
        self.year = re.search( r'(\d{4})', self.season).group()
        self.pool = multiprocessing.cpu_count()


    def check_fixture_diffs(self, data):
        try:
            timestamp = data['kickoff']['millis']
            if self.today <= timestamp:
                return True
        except KeyError as e:
            return False

    def get_fixture_diffs(self):
        if check_fixture_diffs:
            pass



    def file_types(self, file_type):
        types = {'f_stats': 'fixturestats.json',
                 'p_stats': 'playerstats.json',
                 't_squad': 'teamsquads.json',
                 't_stand': 'teamstandings.json',
                 'l_stats': 'league_standings.json'}
        return types.get(file_type)

    def fixture_info_singel(self, fixture_id):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/fixtures/{fixture_id}')
        return ds

    def check_if_stats_exist(self, file_type):
        """Checks if json file exists.

        Args:
            filename(str): The name of the file
            path(str): The path to were the content is to be saved

        """
        file_stats = self.file_types(file_type)
        filename = self.league + '_' + self.year + '_' + file_stats
        try:
            self.dir.load_json(filename, StorageConfig.STATS_DIR)
            return filename
        except FileNotFoundError as e:
            return False

    def check_diff_single(self, data):
        stats_diff = []
        stats = {}
        d_id = data['info']['id']
        new_data = self.fixture_info_singel(d_id)
        stats[d_id] = []
        mismatch = {key for key in data.keys() & new_data if data[key] != new_data[key]}
        if mismatch:
            stats[d_id].append(missmatch)
            stats_diff.append(stats)
        return stats_diff

    def check_diff(self, file):
        filename = self.check_if_stats_exist(file)
        if filename:
            data = self.dir.load_json(filename, StorageConfig.STATS_DIR)

            with Pool(self.pool) as p:
                team_squads = list(tqdm(p.imap(self.check_diff_single, data), total=len(data)))
            return team_squads
        else:
            print('No diffs')
                
        
            

        


class Stats:
    dir = Directory()
    def __init__(self):
        """Creates a pickle object where the __init__() attributes from
        SeasonStats is saved. This is to enable the download of stats
        without having to initiate SeasonStats everytime to download
        stats. Drawback is that the pickled object can get outdated as
        players switch teams or teams move up and down the leagues at
        the ens of the season.
        """

        data = self.dir.load_json('season_params.json', StorageConfig.PARAMS_DIR)
        holder = {str(league)+'_'+ str(season_label):
                    SeasonStats(league=league, season=season_label) 
                        for league, seasons in data.items() for season_label in seasons}
        with open('league_seasons_init', 'wb') as f:
            pickle.dump(holder, f)


if __name__ == '__main__': 
    

    stats = SeasonStatsUpdate('EN_PR', '2019/2020')
    # print(stats.check_diff('f_stats'))




    # season_params = {'EN_PR':['2019/2020', '2018/2019']}
    # gen = ((str(league)+'_'+ str(season_label), SeasonStats(league=league, season=season_label)) for league, seasons in season_params.items() for season_label in seasons)
    # d = dict(gen)
    # with open('test_pickle', 'wb') as f:
    #     pickle.dump(d, f)
    # start = time.time()
    #season_19_20 = SeasonStats('EN_PR', '2018/2019')
    #season_19_20.team_squad()
    # season_19_20.player_stats()
    # season_19_20.fixture_stats()
    # # end = time.time()
    # print(end - start)
