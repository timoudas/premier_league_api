#import os
#import json
import requests
from directory import Directory

Dir = Directory() #

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
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        }

        Dir.mkdir('..', 'json') #Create the json directory if not done

    def get_teams(self):
        """get Ids for all clubs on API, returns a .json file saved in ../json/clubs/clubs.json
        
        json file contains IDs for each club in the API.    
        """
        teams_id = {} #Store all clubs
        url = self.team_id_url
        page = 0 #starting value of page
        while True:
            params = (
                ('pageSize', '100'),
                ('page', str(page))
                    )
            
            # request to obtain the club info
            response = requests.get(url, params = params, headers=self.headers).json()          
            all_clubs = response["content"]
            #loop to get all info for all competitions
            for club in all_clubs: 
                teams_id[club['name']] = club['teams'][0]['id']

            page += 1
            if page == response["pageInfo"]["numPages"]:
                break

        Dir.save_json('team_id', teams_id, '..', 'json') #Save in /json


    def get_competion_id(self):
        """get Ids for competitions on API, returns a .json file saved in 
        ../json/competitions/competitions.json    
        json file contains IDs for each competition in the API.
        """

        url = self.competition_id_url
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        # request to obtain the id values and corresponding competition
        response = requests.get(url, params=params, headers=self.headers).json()
        all_comps = response["content"]
        competitions = {} #Dict that holds all data from API

        for comp in all_comps: #Iterate over all items in the API
            competition_id = comp['description'] #Get dict parent-keys
            index = competition_id #Set parent-keys as index for the the dict
            competitions[index] = \
                 {
                 'abbreviation': comp["abbreviation"],
                  'id' : comp['id'],
                 }
            
        #Save dict to json
        Dir.save_json('competition_id', competitions, '..', 'json') #Save in /json

    def create_leauge_folder(self):
        competitions = Dir.load_json('competition_id.json','..', 'json') #Loag competitions_id file
        competitions_name = [str(comp) for comp in competitions.keys()]
        print(competitions_name)
        for comp_name in competitions_name:
            Dir.mkdir('..','json', comp_name)

    def competition_info(self):
        """Returns id and name of competition in zipped list"""
        competitions = Dir.load_json('competition_id.json', '..', 'json') #Loag competitions_id file
        competitions_id = [str(int(comp['id'])) for comp in competitions.values()]
        competitions_name = [str(comp) for comp in competitions.keys()]
        comp_info = zip(competitions_id, competitions_name)
        return comp_info

    def get_all_compseasons(self):
        """Gets compseasons for all the competition on API and creates a .json file with 
        compseasons for each competion seperatly """
        comp_info = self.competition_info()
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        for comp_id, comp_name in comp_info:
            url = self.base_url + '/competitions/{}/compseasons'.format(comp_id)
            response = requests.get(url, params=params, headers=self.headers).json()
            all_compseasons = response['content']
            seasons = {}
            index = comp_id
            seasons[index] = all_compseasons
            Dir.save_json(comp_name + '_seasons', seasons, '..', 'json', comp_name)






if __name__ == '__main__':
    prem = ApiScraper()
    #prem.get_teams()
    #prem.get_competion_id()
    prem.create_leauge_folder()
    prem.get_all_compseasons()
    

