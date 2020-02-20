#Create one Json file that contains all id information in pure dict format
#So that one can query it easily with the help of ids
#

import requests
from directory import Directory
from pprint import pprint

Dir = Directory() 

class ApiScraper:

    def __init__(self, base_url='https://footballapi.pulselive.com/football'):
        """
        Initializes the base_url for the API and the working directory
        """
        #self.competitions_id = {}
        self.base_url =  base_url 
        self.team_id_url = base_url + '/clubs' ##Set url for teams
        self.competition_id_url = base_url + '/competitions' #Set url for competitions
        #Required header to not get 403-Error from API
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        }


    def competition_info(self):
        competitions_id = self.get_competitions()
        """Returns id and name of competition in zipped list"""
        competition_id = [str(int(comp)) for comp in competitions_id.keys()]
        competition_name = [comp for comp in competitions_id.values()]
        comp_info = zip(competition_id, competition_name)
        return comp_info

    def get_competitions(self):
        """get Ids for competitions on API, returns a .json file saved in 
        ../json/competitions/competitions.json    
        json file contains IDs for each competition in the API.
        """
        competitions_id = {}
        url = self.competition_id_url
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        # request to obtain the id values and corresponding competition
        response = requests.get(url, params=params, headers=self.headers).json()
        all_comps = response["content"]
        competitions = {} #Dict that holds all data from API

        for comp in all_comps: #Iterate over all items in the API
            competition_id = str(int(comp['id'])) #Get dict parent-keys
            index = competition_id #Set parent-keys as index for the the dict
            competitions_id[index] = \
                 {
                 'abbreviation': comp["abbreviation"],
                  'description' : comp['description'],
                 }
        return competitions_id


    def get_compseason(self): 
        competitions_id = self.get_competitions()
        competition_seasons = {}
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        comp_info = self.competition_info()
        for comp_id, comp_name in comp_info:
            url = self.base_url + '/competitions/{}/compseasons'.format(comp_id)
            response = requests.get(url, params=params, headers=self.headers).json()
            all_compseasons = response['content']
            index = comp_id
            competition_seasons[index] = {'seasons': {}}
            for comp in all_compseasons:
                competition_seasons[index]['seasons'][comp['id']]={'label' : comp['label']}
        competitions_id.update(competition_seasons)
        return competitions_id


    def index_compseason(self):
        competitions_id = [str(comp['seasons']) for comp in self.competitions_id.values()]

        print(competitions_id)

    def main(self):
        self.get_competitions()
        self.competition_info()
        self.get_compseason()
        Dir.save_json('test', self.get_compseason(), '..')
        #self.index_compseason()


    # def get_teams(self):




    #     for comp_season in 
    #     url = self.base_url + '/teams'
    #     params = (('pageSize', '100'),
    #                 ('compSeasons', str(comp_season)))#adds ?pageSize=100 to url


            
if __name__ == '__main__':
    prem = ApiScraper()
    prem.main()
            
