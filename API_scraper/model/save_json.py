from directory import Directory
import requests
from pprint import pprint

headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        }

Dir = Directory() 
file = Dir.load_json('test.json')

league = {}
competition_ids = [1,2,3,4,5,6]
comp_name = ['a', 'b', 'c', 'd', 'e', 'f']

comp_info = zip(competition_ids, comp_name)
#Retreives all competietion seasons and forms dictionairies
for name in comp_name:
    league = {name:{}}

for season_id, comp_name in comp_info:
    params = (('pageSize', '100'),)#adds ?pageSize=100 to url
    url = 'https://footballapi.pulselive.com/football/competitions/{}/compseasons'.format(season_id)
    response = requests.get(url, params=params, headers=headers).json()
    all_compseasons = response['content']
    index = comp_name
    league[index] = {'seasons': {}}
    for comp in all_compseasons:
        league[comp_name]['seasons'][comp['id']]={'label' : comp['label']}

pprint(league)









# parent_key = [key for key in file.keys()]
# comp_ids = [comp_id['id'] for comp_id in file.values()]
# info = zip(parent_key, comp_ids)
# season_id = []
# for key,ids in info:
#     #print(key, ids)
#      seasons = file[key]['seasons']
#      for season in seasons:
#         if season in seasons:
#             i = tuple(season['id'], ids)
#             season_id.append(i)

# print(season_id)


# for comp_id in comp_ids:
#   print(comp_id)
#   for comp_season in season_id:
#       print(comp_season)
        # url = 'https://footballapi.pulselive.com/football/teams'
        # params = (('pageSize', '100'),
        #         ('comps', str(comp_id)),
        #           ('compSeasons', str(comp_season)),
        #                                            )#adds ?pageSize=100 to url
        # response = requests.get(url, params=params, headers=headers).json()
        # print(response)



import json
import requests

layer1 = 'https://footballapi.pulselive.com/football/competitions'
layer2 = 'https://footballapi.pulselive.com/football/competitions/1/compseasons'
layer3 = 'https://footballapi.pulselive.com/football/teams?comps=1&pageSize=100&compSeasons=274'
layer4 = 'https://footballapi.pulselive.com/football/teams/1/compseasons/274/staff'


def view_raw_input(url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
              }
    response = requests.get(url, headers=headers).json()
    data = response['content']
    print(data)


#Psuedo-Example on how Ids are retreived and merged
class ApiScraper:

    def __init__(self, base_url='https://footballapi.pulselive.com/football'):
        """
        Initializes the base_url for the API and the working directory
        """
        self.base_url =  base_url 
        self.team_id_url = base_url + '/clubs' ##Set url for teams
        self.competition_id_url = base_url + '/competitions' #Set url for competitions
        #Required header to not get 403-Error from API
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 
                        }

    def get_competitions(self):
        """get Ids for competitions on API, returns a dict"""

    def get_compseason(self):
        """get Ids for competition_seasons on API, returns a dict"""

    def get_teams(self):
        """gets Ids for teams in a given competition_seasons, returns a"""

    def get_players(self):







