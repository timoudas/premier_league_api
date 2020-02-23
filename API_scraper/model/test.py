import json
import requests
from pprint import pprint
from directory import Directory

layer1 = 'https://footballapi.pulselive.com/football/competitions' #League Ids
layer2 = 'https://footballapi.pulselive.com/football/competitions/1/compseasons'#Season Ids for League_id: 1
layer3 = 'https://footballapi.pulselive.com/football/teams?comps=1&pageSize=100&compSeasons=274'#Teams_Ids for League_id: 1, Season_id:274
layer4 = 'https://footballapi.pulselive.com/football/teams/1/compseasons/274/staff' #Players_Ids for team_id: 1, Season_id:274


def load_raw_data(url):
    """Retreives Ids for different pages on the API"""
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
    elif "fixtures" in url:
        data = response
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

class FixtureInfo(dict):
    _fixtures = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_info_for_fixture(self, fixture):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/fixtures/{fixture}')
        self.clear()
        for d in ds:
            self._fixtures[d['id']] = d
            self[d['id']] = self._fixtures[d['id']]
        return self._fixtures

        
       
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
            self['competition'] = competition
            self.players = TeamPlayers()#Returns Ids and info for every player on a team

        def load_players(self):
            """returns info for all the players given their id and a season _id"""
            self.players.load_players_for_team(self['id'], self['competition'])

    def load_teams_for_season(self, season, comp):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams?comps={comp}&pageSize=100&compSeasons={season}')
        self.clear()
        for d in ds:
            d['competition'] = comp
            self._teams[d['id']] = self.Team(comp, d)
            self[d['shortName']] = self._teams[d['id']]
        return self._teams

#NO IDE HOW THIS WORKS - REPLICATE SeasonTeams
class SeasonFixtures(dict):
    """Creates an object for all fixtures in a given a season """
    _fixtures = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Fixture(dict):
        """Creates an object for a fixture in a competion and specific season"""

        def __init__(self, fixture, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['fixture'] = fixture
            self.fixture = FixtureInfo()#Returns Ids and info for every player on a team

        def load_fixture(self):
            """returns info for a fixture given it's Id"""
            self.fixture.load_info_for_fixture(self['id'])

    def load_fixture_for_season(self, season):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/fixtures?compSeason={season}')
        self.clear()
        for d in ds:
            d['fixture'] = season
            self._fixtures[d['id']] = self.Fixture(season, d)
            self[d['shortName']] = self._fixtures[d['id']]
        return self. _fixtures
    

class Season(dict):
    all_teams = SeasonTeams()

    def __init__(self, competition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['competition'] = competition
        self.teams = SeasonTeams()
        self.fixtures = SeasonFixtures()

    def load_teams(self):
        self.teams.load_teams_for_season(self['id'], self['competition'])

    def load_played_fixtures(self):
        self.fixtures.load_fixture_for_season(self['id'])

    def load_unplayed_fixtures(self):
        pass

    def load_all_fixtures(self):
        pass


class League(dict):
    """Gets Season_ids, returns a dict"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seasons = {} #Initates dictionairy to hold seasonIds

    def load_seasons(self):
        """Returns a dict with season label as key and season id as value"""
        ds = load_raw_data(f'https://footballapi.pulselive.com/football/competitions/{self["id"]}/compseasons')
        self.seasons = {d['label']: Season(self['id'], d) for d in ds}
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


Dir = Directory() 
fb = Football()
fb.load_leagues()
fb.leagues['EN_PR'].load_seasons()
fb.leagues['EN_PR'].seasons['2019/20'].load_played_fixtures()


#We want to query 
#fb.leagues['EN_PR'].seasons['2019/20'].load_played_fixtures()
#fb.leagues['EN_PR'].seasons['2019/20'].load_unplayed_fixtures()
#fb.leagues['EN_PR'].seasons['2019/20'].load_all_fixtures()



pprint(fb.leagues['EN_PR'].seasons)


#pprint(fb.leagues['EN_PR'].seasons['2019/20'].load_teams())


#leagues = [league for league in fb.load_leagues().keys()]
#league_names = [league['description'] for league in fb.load_leagues().values()]
#print(leagues)
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