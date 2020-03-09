from api_scraper import Football
from pprint import pprint
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import sys
from directory import Directory
import requests
import re



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

class Stats():
    """Object to instansiate a league and season pair
    
    Args:
        league(str): league_id
        season(str): season_id
    """
    fb = Football()
    dir = Directory()
    def __init__(self, league='EN_PR', season='2019/2020'):
        self.pool = multiprocessing.cpu_count()
        self.league = league
        self.season = season
     
    def load_season_fixture(self):
        """Loads the fixtures for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season}')
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()

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
            players = self.fb.leagues[self.league].seasons['2019/2020'].teams[team['shortName']].load_players()
        for player in players.keys():
            player_id.append(player)
        print('Initialization completed')
        return player_id

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

class GameStats(Stats):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fixture_id = [fix['id'] for fix in self.load_season_fixture().values()]

    def fixture_stats_singel(self, fixture):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
        return ds

    def fixture_stats(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats = {}
        print("Getting fixture stats..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_id, chunksize=1), total=len(self.fixture_id)))
        print('Getting data from workers..')
        i = 0
        for fixture in fixture_stats:
            game_id = fixture['entity']['id'] #Get's the gameIDs for each game
            index = game_id #Set's gameIDs as index for dictionairy
            stats[index] = {'info': fixture['entity']}
            if 'data' in fixture:
                stats[index].update({'stats':fixture['data']})
            else:
                i += 1

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        year = re.search( r'(\d{4})', self.season).group()  
        filename = self.league + '_' + year + '_' + 'fixturestats'
        self.dir.save_json(filename, stats, '..', 'json', 'params')
        path = '/'.join(('..', 'json', 'params'))
        print(f'Saved as {filename}.json in {path}')

class PlayerStats(Stats):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.player_id = self.load_season_players()

    def player_stats_singel(self, player):
        #NEED TO HAVE SEASON ID
        season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/stats/player/{player}?compSeasons={season_id}')
        return ds

    def player_stats(self):
        stats = {}
        print("Getting player stats..")
        with Pool(self.pool) as p:
            player_stats = list(tqdm(p.imap(self.player_stats_singel, self.player_id, chunksize=1), total=len(self.player_id)))
        print('Getting data from workers..')
        all_players = player_stats
        i = 0
        for player in all_players:
            game_id = int(player['entity']['id']) #Get's the gameIDs for each game
            index = game_id #Set's gameIDs as index for dictionairy
            stats[index] = {'info': player['entity']}
            if 'stats' in player:
                stats[index].update({'stats':player['stats']})
            else:
                i += 1

        print('Completed')
        if i > 0:
            print(f'{i} players retreived had no stats')
        year = re.search( r'(\d{4})', self.season).group()  
        filename = self.league + '_' + year + '_' + 'playerstats'
        self.dir.save_json(filename, stats, '..', 'json', 'params')
        path = '/'.join(('..', 'json', 'params'))
        print(f'Saved as {filename}.json in {path}')

class TeamStandings(Stats):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.team_id = [fix['id'] for fix in self.load_season_teams().values()]

    def team_standings_singel(self, team_id):
        #NEED TO HAVE SEASON ID
        season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/compseasons/{season_id}/standings/team/{team_id}')
        return ds

    def team_standings(self):
        stats = {}
        print("Getting team standings..")
        with Pool(self.pool) as p:
            team_standings = list(tqdm(p.imap(self.team_standings_singel, self.team_id, chunksize=1), total=len(self.team_id)))
        print('Getting data from workers..')
        i = 0
        team_standing = team_standings
        for team in team_standing:
            team_id = int(team['team']['club']['id']) #Get's the gameIDs for each game
            index = team_id #Set's gameIDs as index for dictionairy
            if 'compSeason' in team:
                stats[index] = {'season': team['compSeason']}
            if 'team' in team:
                stats[index].update({'team': team['team']})
            if 'entries' in team:
                stats[index].update({'standing': team['entries']})
            else:
                i += 1

        print('Completed')
        if i > 0:
            print(f'{i} teams retreived had no standings')
        year = re.search( r'(\d{4})', self.season).group()  
        filename = self.league + '_' + year + '_' + 'teamstandings'
        self.dir.save_json(filename, stats, '..', 'json', 'params')
        path = '/'.join(('..', 'json', 'params'))
        print(f'Saved as {filename}.json in {path}')


def main():
    game_stats = GameStats()
    player_stats = PlayerStats()
    team_standings = TeamStandings()
if __name__ == '__main__':
    main()





start = time.time()
d = TeamStandings()
d.team_standings()
end = time.time()
print(end - start)






