import requests
from pprint import pprint
import re


#TODO
"""
*Program is not scaling well

"""

"""***HOW TO USE***

    1. Create an instance of Football, this initiates the leagues dict which holds
    all the leagueIDs.

    fb = Football()

    2. To get the all the seasons for all leagues, first run the the method
    fb.load_leagues()
    this fills the leagues dict with nessesery info to make further querys.
    To get season values the league abbreviation has to be passed like below:

    fb.leagues['EN_PR'].load_seasons()

    This selects the key 'EN_PR' which is the parent key in leagues and loads
    the season for that league by running the method load.seasons() which is in
    class Leagues(). This returns a dict seasons holding the following:

    1992/93': {'competition': 1, 'id': 1, 'label': '1992/93'}

    Where the '1992/93' is the key containing that seasons information.


    ***WHAT IS NEEDED FOR ARBITRAIRY QUERYS***

    League abbreviation
    Season label
    Team name

    """


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
        if page >= response["pageInfo"]["numPages"]:
            break

    for d in data_temp:
        d['id'] = int(d['id'])
    return data_temp



class TeamPlayers(dict):
    _players = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_players_for_team(self, team, season):
        #self.clear()
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/teams/{team}/compseasons/{season}/staff')
        for d in ds:
            if d:
                self._players[d['id']] = d
                self[d['id']] = self._players[d['id']]
        return self._players

class FixtureInfo(dict):
    _fixtures = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_info_for_fixture(self, season):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/fixtures?compSeasons={season}')
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
        self._teams.clear()
        for d in ds:
            d['competition'] = comp
            self._teams[d['id']] = self.Team(season, d)
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

        def __init__(self, competition, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['competition'] = competition
            self.fixture = FixtureInfo()#Returns Ids and info for every player on a team
        def load_fixture(self):
            """returns info for a fixture given it's Id"""
            self.fixture.load_info_for_fixture(self['id'])

    def load_fixture_for_season(self, season):
        ds = load_raw_data(
            f'https://footballapi.pulselive.com/football/fixtures?compSeasons={season}')
        self.clear()
        for d in ds:
            d['competition'] = season
            self._fixtures[d['id']] = self.Fixture(season, d)
            self[d['status']] = self._fixtures[d['id']]
        return self._fixtures

class Season(dict):
    all_teams = SeasonTeams()


    def __init__(self, competition,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['competition'] = competition
        self.teams = SeasonTeams()
        self.fixtures = SeasonFixtures()

    def load_teams(self):
        return self.teams.load_teams_for_season(self['id'], self['competition'])


    def load_played_fixtures(self):
        return self.fixtures.load_fixture_for_season(self['id'])

    def load_unplayed_fixtures(self):
        pass

    def load_all_fixtures(self):
        pass


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


if __name__ == '__main__':

    # Dir = Directory() 
    fb = Football()
    # lg = League()
    # fx = FixtureInfo()
    fb.load_leagues()
    # ds = fb.leagues['EN_PR'].load_seasons()
    # fb.leagues['EN_PR'].seasons['2016/2017'].load_teams()
    # pprint(fb.leagues['EN_PR'].seasons['2016/2017'].teams['Arsenal'].load_players())
    ds = fb.leagues['EU_CL'].load_seasons()
    fb.leagues['EU_CL'].seasons['2016/2017'].load_teams()
    pprint(fb.leagues['EU_CL'].seasons['2016/2017'].teams['Atlético'].load_players())

    #pprint(fb.leagues['EN_PR'].seasons['2018/2019'].load_teams())
    #pprint(fb.leagues['EN_PR'].seasons['2018/2019'].teams['Aston Villa'].load_players())

    #id = [i['id'] for i in fb.leagues['EN_PR'].seasons['2019/2020'].keys()]

    # ds = fb.leagues['EN_PR'].seasons['2019/2020'].load_teams()
    # fb.leagues['EN_PR'].seasons['2019/2020'].teams['Wolves'].load_players()
    #         print('Sucesess')
    #     except:
    #         print(d['shortName'], "didn't work")
    #         print('Nooooo')


    # fb = Football()
    # fb.load_leagues()
    # fb.leagues['EN_PR'].load_seasons()
    # ds = fb.leagues['EN_PR'].seasons['2019/2020'].load_teams()
    # """Retreives Ids for different pages on the API"""
    # headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #                'Origin': 'https://www.premierleague.com',
    #                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    # params = (('pageSize', '100'),)

    # for s in ds.values():
    #     i = s['id']
    #     print(i)
    #     url = f'https://footballapi.pulselive.com/football/teams/{i}/compseasons/274/staff'
    #     # request to obtain the team info
    #     try:
    #         response = requests.get(url, headers=headers, params=params).json()
    #         print(response['team']['name'])
    #     except Exception as e:
    #         print(i)
    #         print(url)
    #         print(s['club']['shortName'])
    #         print(e, 'Something went wrong with the request')
    #         time.sleep(2)


    

    #ds = (load_raw_data('https://footballapi.pulselive.com/football/competitions'))
    #l = [d['abbreviation'] for d in ds]
    #league = fb.load_leagues()
    #pprint(fb.leagues['EU_CL'].load_seasons())







    #fb.leagues['EN_PR'].load_seasons()

    #
    #print(fb.leagues['EN_PR'].seasons['2019/20'].load_teams())
    #fb.leagues['EN_PR'].seasons['2019/20'].load_played_fixtures()

    #pprint(len(FixtureInfo().load_info_for_fixture(274).keys()))
    #pprint(TeamPlayers().load_players_for_team(1, 274).keys())



    #We want to query 

    #fb.leagues['EN_PR'].seasons['2019/20'].load_unplayed_fixtures()
    #fb.leagues['EN_PR'].seasons['2019/20'].load_all_fixtures()



    # pprint(fb.leagues['EN_PR'].seasons)


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