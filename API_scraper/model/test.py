from api_scraper import *
from pprint import pprint
from tqdm import tqdm

"""         // Lists all the statistics for a given match
            // Params : compSeasonIds, sort, sys
            'match' : '/stats/match/{id}',
            // Lists all the statistics for a given player
            // Params : compSeasonIds, sort, fixtures, comps, sys
            'player' : '/stats/player/{id}',"""
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
                ('page', str(page)))

    # request to obtain the team info
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

class PremierLeague():
    fb = Football()
    def __init__(self):
        self.leagues = self.fb.load_leagues()
        self.seasons = self.fb.leagues['EN_PR'].load_seasons()
        self.fixture_id = self.get_fixtures

    
    def get_fixtures(self):
        fixture_id = []
        for season in tqdm(self.seasons.values()):
            comp_season = season['id']
            ds = load_raw_data(f'https://footballapi.pulselive.com/football/fixtures?compSeasons={comp_season}')
            for d in ds:
                fixture_id.append(d['id'])
        return fixture_id
            
      def fixture_stats(self):
        for fixture in tqdm(self.fixture_id):
            ds = load_raw_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
            print(ds)




d = PremierLeague()
d.fixture_stats()




