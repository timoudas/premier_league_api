from api_scraper import Football
from pprint import pprint
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import json
import sys
from directory import Directory
from directory import StorageConfig
import requests
import re
import pickle
import os
import argparse



"""         // Lists all the statistics for a given match
            // Params : compSeasonIds, sort, sys
            'match' : '/stats/match/{id}',
            // Lists all the statistics for a given player
            // Params : compSeasonIds, sort, fixtures, comps, sys
            'player' : '/stats/player/{id}',"""

def load_raw_data(url):
    """Makes requests against the API
        Args:
            url(str): The url that is to be requested

        Returns the json data from the url
    """
    page = 0
    data_temp = [] #Placeholder when url has multiple pages
    #Loops all the pages on the requested url
    while True:
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        params = (('pageSize', '100'),
                ('page', str(page),))

        #try to obtain the json-data from the url
        try:
            response = requests.get(url, params = params, headers=headers).json()  
            if url.endswith('staff'):
                data = response['players']
                return data
            elif 'fixtures' in url:
                data = response["content"]
                #loop to get info for each game
                data_temp.extend(data)
            else:
                data = response['content']
                # note: bit of a hack, for some reason 'id' is a float, but everywhere it's referenced, it's an int
                for d in data:
                    d['id'] = int(d['id'])
                return data
        except Exception as e:
            print(e, 'Something went wrong with the request')
            return {}

        page += 1
        if page == response["pageInfo"]["numPages"]:
            break

    for d in data_temp:
        d['id'] = int(d['id'])
    return data_temp

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

class SeasonStats:
    fb = Football()
    dir = Directory()

    def __init__(self, league, season):
        

        ### Included from '__init__'s of previous subclasses ###
        self.pool = multiprocessing.cpu_count()
        self.league = league
        self.season = season
        self.fixture_ids = [fix['id'] for fix in self.load_season_fixture().values()]
        self.team_ids = [team['id'] for team in self.load_season_teams().values()]
        self.player_ids = self.load_season_players()
        self.dir.mkdir('..', 'json', 'params', 'stats')
        self.year = re.search( r'(\d{4})', self.season).group()

    def save_completed(self, filename, stats_list, path):
        year = re.search( r'(\d{4})', self.season).group()  
        filename = self.league + '_' + year + '_' + filename
        self.dir.save_json(filename, stats_list, StorageConfig.STATS_DIR)
        print(f'Saved as {filename}.json in {path}')

    def load_season_fixture(self):
        """Loads the fixtures for a league-season,
        calls api_scraper.py methods
        """
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print(f'Initializing \t {self.league} \t {self.season} fixtures')
        print('Initialization completed')
        self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()
        return self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()

    def load_season_teams(self):
        """Loads the teams for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} teams')
        player_id = []
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_teams()

    def load_season_players(self):
        """Loads the players for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} players')
        player_id = []
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        teams = self.fb.leagues[self.league].seasons[self.season].load_teams()
        for team in tqdm(teams.values()):
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

    def fixture_stats_singel(self, fixture):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
        return ds

    def fixture_stats(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats_list = []
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print("Getting fixture stats..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for fixture in fixture_stats:
            stats = {}
            if 'data' in fixture:
                stats['info'] = fixture['entity']
                stats['stats'] = fixture['data']
            else:
                i += 1
            if stats:
                stats_list.append(stats)

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('fixturestats', stats_list, StorageConfig.STATS_DIR)

    def player_stats_singel(self, player):
        season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/stats/player/{player}?compSeasons={season_id}')
        return ds

    def player_stats(self):
        stats_list = []
        # stats = {}
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print("Getting player stats..")
        with Pool(self.pool) as p:
            player_stats = list(tqdm(p.imap(self.player_stats_singel, self.player_ids), total=len(self.player_ids)))
        print('Getting data from workers..')
        all_players = player_stats
        i = 0
        for player in all_players:
            stats = {"info": {}}
            stats["info"] = player['entity']
            if 'stats' in player:
                stats['stats'] = player['stats']
                stats['stats'].append({'id':player['entity']['id']})
            elif not player['stats']:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} players retreived had no stats')
        self.save_completed('playerstats', stats_list, StorageConfig.STATS_DIR)

    def team_standings_singel(self, team_id):
        #NEED TO HAVE SEASON ID
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/compseasons/{season_id}/standings/team/{team_id}')
        return ds

    def team_standings(self):
        stats_list = []
        print("Getting team standings..")
        with Pool(self.pool) as p:
            team_standings = list(tqdm(p.imap(self.team_standings_singel, self.team_ids), total=len(self.team_ids)))
        print('Getting data from workers..')
        i = 0
        team_standing = team_standings
        for team in team_standing:
            stats = {"season": {}, "team": {}, "standing": {}}
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

class Stats:
    dir = Directory()
    def __init__(self):

        data = self.dir.load_json('season_params.json', '..', 'json', 'params')
        holder = {str(league)+'_'+ str(season_label):
                    SeasonStats(league=league, season=season_label) 
                        for league, seasons in data.items() for season_label in seasons}
        with open('league_seasons_init', 'wb') as f:
            pickle.dump(holder, f)







#stat = Stats()



if __name__ == '__main__': 
    pass

    #stats = SeasonStats()
    # season_params = {'EN_PR':['2019/2020', '2018/2019']}
    # gen = ((str(league)+'_'+ str(season_label), SeasonStats(league=league, season=season_label)) for league, seasons in season_params.items() for season_label in seasons)
    # d = dict(gen)
    # with open('test_pickle', 'wb') as f:
    #     pickle.dump(d, f)
    # start = time.time()
    # season_19_20 = SeasonStats('EN_PR', '2018/2019')
    # season_19_20.team_standings()
    # season_19_20.player_stats()
    # season_19_20.fixture_stats()
    # # end = time.time()
    # print(end - start)
