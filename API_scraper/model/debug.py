from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import sys
import requests
import re
from pprint import pprint


def load_raw_data(url):
    """Retreives Ids for different pages on the API"""
    page = 0
    data_temp = []
    while True:
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        params = (('pageSize', '100'),
                 ('page', str(page),))

    # request to obtain the team info
        try:
            response = requests.get(url, headers=headers, params=params).json()
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


class TeamPlayers(dict):
    _players = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_players_for_team(self, team, season):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams/{team}/compseasons/{season}/staff')
        self.clear()
        for d in ds:
            self._players[d['id']] = d
            self[d['id']] = self._players[d['id']]
        return self._players



class SeasonTeams(dict):
    """Creates an object for a team given a season """
    _teams = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Team(dict):
        """Creates an object for a team in a competion and specific season

        Args:
            competition (str): Competition abbreviation
        """
        def __init__(self, competition, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['competition'] = competition ##THIS IS THE PROBLEM##############################################
            #self['season'] = season #######################TRYING TO SOLVE
            self.players = TeamPlayers()#Returns Ids and info for every player on a team

        def load_players(self):
            """returns info for all the players given their id and a season _id"""
            return self.players.load_players_for_team(self['id'], self['competition'])

    def load_teams_for_season(self, season, comp):

        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams?comps={comp}&compSeasons={season}')
        self.clear()
        for d in ds:
            d['competition'] = comp
            self._teams[d['id']] = self.Team(season, d)
            self[d['shortName']] = self._teams[d['id']]
        return self._teams

class Season(dict):
    all_teams = SeasonTeams()

    def __init__(self, competition,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['competition'] = competition
        self.teams = SeasonTeams()

    def load_teams(self):
        return self.teams.load_teams_for_season(self['id'], self['competition'])


class League(dict):
    """Gets Season_ids, returns a dict"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seasons = {} #Initates dictionairy to hold seasonIds

    def season_label(self, label):
        try:
            return re.search( r'(\d{4}/\d{4})', label).group()  
        except: 
            label = re.search( r'(\d{4}/\d{2})', label).group()
            return re.sub(r'(\d{4}/)', r'\g<1>20', label)


    def load_seasons(self):
        """Returns a dict with season label as key and season id as value"""
        ds = load_raw_data(f'https://footballapi.pulselive.com/football/competitions/{self["id"]}/compseasons')
        self.seasons = {self.season_label(d['label']): Season(self['id'], d) for d in ds}
        return self.seasons


class Football:
    """Gets Competition_abbreviation, returns a dict"""
    def __init__(self):
        self.leagues = {} #Initates dictionairy to hold leagueIds

    def load_leagues(self):
        """Returns a dict with league abbreviation as key and league id as value"""
        ds = load_raw_data('https://footballapi.pulselive.com/football/competitions')
        self.leagues = {d['abbreviation']: League(d) for d in ds}
        return self.leagues

class SeasonStats:
    fb = Football()

    def __init__(self, league, season):
        

        ### Included from '__init__'s of previous subclasses ###
        self.league = league
        self.season = season
        self.player_ids = self.load_season_players()

    def load_season_players(self):
        """Loads the players for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} players')
        player_id = []
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        teams = self.fb.leagues[self.league].seasons[self.season].load_teams()
        print(len(teams))

        for team in tqdm(teams.values()):

            players = self.fb.leagues[self.league].seasons[self.season].teams[team['shortName']].load_players()
        for player in players.keys():
            player_id.append(player)
        print('Initialization completed')
        return player_id

def main():
    try:
        season_params = {'EN_PR':['2019/2020', '2018/2019']}
        gen = ((str(league)+'_'+ str(season_label), SeasonStats(league=league, season=season_label)) for league, seasons in season_params.items() for season_label in seasons)
        dict(gen)
    except Exception as e:
        print(e)


if __name__ == '__main__': 

    main()




