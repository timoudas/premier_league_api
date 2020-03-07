from api_scraper import *
from pprint import pprint
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import sys
from directory import Directory



"""         // Lists all the statistics for a given match
            // Params : compSeasonIds, sort, sys
            'match' : '/stats/match/{id}',
            // Lists all the statistics for a given player
            // Params : compSeasonIds, sort, fixtures, comps, sys
            'player' : '/stats/player/{id}',"""

#Example query
#pl = PremierLeague()
#pl.season['2019/2020'].load_fixtures()

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

def import_id(file_id):
    return dir.load_json(file_id ,'..', 'json', 'params')


class FixtureSeasons():
    fb = Football()
    dir = Directory()
    def __init__(self, league='EN_PR'):
        self.league = league
        self.api = self.fb.load_leagues()
        self.seasons = {}
        self.pool = multiprocessing.cpu_count()
        

    def get_season(self):
        league_seasons = self.api[self.league].load_seasons()
        self.seasons = {label: label_id['id'] for label, label_id in league_seasons.items()}


class FixtureStats(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = {} 

    def load_fixtures(self, fixture):
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{self["id"]}')
        #self.seasons = {self.season_label(d['label']): Season(self['id'], d) for d in ds}
        return self.seasons


start = time.time()
d = FixtureSeasons()
d.get_season()
print(d.seasons)

