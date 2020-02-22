import json
import requests
from pprint import pprint
from directory import Directory

layer1 = 'https://footballapi.pulselive.com/football/competitions' #League Ids
layer2 = 'https://footballapi.pulselive.com/football/competitions/1/compseasons'#Season Ids for League_id: 1
layer3 = 'https://footballapi.pulselive.com/football/teams?comps=1&pageSize=100&compSeasons=274'#Teams_Ids for League_id: 1, Season_id:274
layer4 = 'https://footballapi.pulselive.com/football/teams/1/compseasons/274/staff' #Players_Ids for team_id: 1, Season_id:274


def load_raw_data(url):
    """View the input data that I use to retrieve the different Ids"""
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
              }
    params = (('pageSize', '100'),)
    try:
        response = requests.get(url, headers=headers, params=params).json()
    except:
        return {}

    if url.endswith('staff'):
        data = response['players']
    else:
        data = response['content']
        # note: bit of a hack, for some reason 'id' is a float, but everywhere it's referenced, it's an int
        for d in data:
            d['id'] = int(d['id'])

    return data


class TeamPlayers(dict):
    _players = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_players_for_team(self, team, comp):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams/{team}/compseasons/{comp}/staff')
        self.clear()
        for d in ds:
            self._players[d['id']] = d
            self[d['id']] = self._players[d['id']]
        return self._players


class SeasonTeams(dict):
    _teams = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Team(dict):
        def __init__(self, competition, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['competition'] = competition
            self.players = TeamPlayers()

        def load_players(self):
            return self.players.load_players_for_team(self['id'], self['competition'])

    def load_teams_for_season(self, season, comp):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams?comps={comp}&pageSize=100&compSeasons={season}')
        self.clear()
        for d in ds:
            d['competition'] = comp
            self._teams[d['id']] = self.Team(comp, d)
            self[d['shortName']] = self._teams[d['id']]
        return self._teams

class Season(dict):
    all_teams = SeasonTeams()

    def __init__(self, competition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['competition'] = competition
        self.teams = SeasonTeams()

    def load_teams(self):
        return self.teams.load_teams_for_season(self['id'], self['competition'])


class League(dict):
    """Gets Season_ids, returns a dict"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seasons = {}

    def load_seasons(self):
        ds = load_raw_data(f'https://footballapi.pulselive.com/football/competitions/{self["id"]}/compseasons')
        self.seasons = {d['label']: Season(self['id'], d) for d in ds}
        return self.seasons


class Football:
    """Gets Competition_abbreviation, returns a dict"""
    def __init__(self):
        self.leagues = {}

    def load_leagues(self):
        ds = load_raw_data('https://footballapi.pulselive.com/football/competitions')
        self.leagues = {d['abbreviation']: League(d) for d in ds}
        return self.leagues

Dir = Directory() 
fb = Football()

# Dir.mkdir('..', 'json')
leagues = [league for league in fb.load_leagues().keys()]
league_names = [league['description'] for league in fb.load_leagues().values()]
print(leagues)
#for league in leagues:
    #print(leagues)
    #seasons = fb.leagues[league].load_seasons()
    #seasons_label = [season['id'] for season in seasons.values()]
    #for season in seasons_label:
        #teams = fb.leagues[leagues].seasons[season].load_teams()



# Dir.save_json('test_teams', fb.leagues['EN_PR'].seasons['2019/20'].load_teams(), '..', 'json')
# Dir.save_json('test_players', fb.leagues['EN_PR'].seasons['2019/20'].teams['Chelsea'].load_players(), '..', 'json')




#fb.leagues['EN_PR'].seasons['2019/20'].load_teams()

# load the players for a specific team
#fb.leagues['EN_PR'].seasons['2019/20'].teams['Chelsea'].load_players()

# or perhaps for all
#for team in fb.leagues['EN_PR'].seasons['2019/20'].teams.values():
    #team.load_players()

#pprint(fb.leagues)
#pprint(fb.leagues['EN_PR'].seasons)
#pprint(fb.leagues['EN_PR'].seasons['2019/20'].teams)
#pprint(fb.leagues['EN_PR'].seasons['2019/20'].teams['Chelsea'].players)

#pprint('goalies:',
      #[player['name']['display']
       #for team in fb.leagues['EN_PR'].seasons['2019/20'].teams.values()
       #for player in team.players.values() if 'position' in player['info'] and player['info']['position'] == 'G'])