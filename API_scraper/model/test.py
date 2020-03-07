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



class PremierLeague():
    fb = Football()
    dir = Directory()
    def __init__(self, league='EN_PR', season='2019/2020'):
        self.pool = multiprocessing.cpu_count()
        self.league = league
        self.season = season
        self.fixture_id = [fix['id'] for fix in self.load_season_fixture().values()]
    


    def load_season_fixture(self):
        print(f'Initializing \t {self.league} \t {self.season}')
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()

    def fixture_stats_singel(self, fixture):
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
        return ds

    def fixture_stats(self):
        stats = {}
        print("Getting fixture stats..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_id, chunksize=1), total=len(self.fixture_id)))
        print('Getting data from workers..')
        fix = fixture_stats
        i = 0
        for fixture in fix:
            game_id = fixture['entity']['id'] #Get's the gameIDs for each game
            index = game_id #Set's gameIDs as index for dictionairy
            stats[index] = {'info': fixture['entity']}
            if 'data' in fixture:
                stats[index].update({'stats':fixture['data']})
        #pprint(stats)       
        # for fixture in fix:
        #     stats.update({fixture['entity']['id']: fixture['entity']})
        #     pprint(fixture['entity'])
        #     if 'data' in fixture:
        #          stats.update({fixture['entity']['id']: fixture['data']})
        #     else:
        #         i+=1

        print('Completed')
        print(f'{i} games retreived had no stats')
        year = re.search( r'(\d{4})', self.season).group()  
        filename = self.league + '_' + year + '_' + 'fixturestats'
        self.dir.save_json(filename, stats, '..', 'json', 'params')
        path = '/'.join(('..', 'json', 'params'))
        print(f'Saved as {filename}.json in {path}')


start = time.time()
d = PremierLeague('EU_CL', '2019/2020')
d.fixture_stats()
end = time.time()
print(end - start)






