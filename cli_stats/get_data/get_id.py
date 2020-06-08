import os
import re
import time


from api_scraper.api_scraper import Football
from directory import Directory
from pprint import pprint
from storage_config import StorageConfig
from tqdm import tqdm

dirs = Directory()




class Params():
    '''
    The Params object contains a methods for retrieving IDs
    for leagues and season in dict-format

    Attributes:
        fb (object): Loads the Football module
        fb.league (method): Calls the load_leagues() method in Football module 
                            to grant league_IDs and names
        dir (object): Load the Directory module
        dir.mkdir (method): Calls the mkdir() method in Directory module
                                creates params folder in json folder if non-existant
    '''
    def __init__(self):
        self.fb = Football()
        self.fb_league = self.fb.load_leagues()
        self.dir = Directory()
        self.dir.mkdir(StorageConfig.PARAMS_DIR)

    @staticmethod
    def season_label(label):
        """Performs RegEx on all season labels
        to match the format dddd/dddd"""
        try:
            return re.search(r'(\d{4}/\d{4})', label).group()  
        except:
            label = re.search(r'(\d{4}/\d{2})', label).group()
            return re.sub(r'(\d{4}/)', r'\g<1>20', label)      

    def league_param(self):
        """Generates a .json with a a league as key and it's id as value
            Ex. {'EN_PR': 1,
                 'EU_CL': 2,}
        """
        league_info = {} #Placeholder-dict for league {name: id}
        #Iterates over all leagues
        for league in tqdm(self.fb_league.values()):
            league_info.update({league['abbreviation']: league['id']})
        #Saves league_info as league_params.json in params folder
        self.dir.save_json('league_params', league_info, StorageConfig.PARAMS_DIR)
        #self.dir.save_json('league_params', league_info, '..', 'json', 'params')

    def league_season_param(self):
        """Generates a .json with a a league_abbreviation as key and a list of dicts
          as value with all season labels and ids in pairs.
            Ex. {'EN_PR':[
                          {'2019/2020': 274},
                          {'2018/2019': 210},
                         ]
                }
        """
        #Gets the league abbreviations from fb_league
        league_abbreviation = [league['abbreviation'] for league in self.fb_league.values()]
        season_info = {} #Placeholder-dict for league-season
        season_info_id = {}
        #Iterates over all league_abbreviations
        for abbreviation in tqdm(league_abbreviation):
            #loads all seasons for each abbreviation
            league_info = self.fb_league[abbreviation].load_seasons()
            season_info[abbreviation] = []#Initiates empty list as value
            season_info_id[abbreviation] = []#Initiates empty list as value
            for i in league_info.values():
                if self.season_label(i['label']).startswith('2'):
                    season_info[abbreviation] += [self.season_label(i['label'])]
                    season_info_id[abbreviation] += [{'label':self.season_label(i['label']) , 'id': i['id']}]
        #Saves season_info as season_params.json in params folder
        self.dir.save_json('season_params', season_info, StorageConfig.PARAMS_DIR)
        self.dir.save_json('season_params_id', season_info_id, StorageConfig.PARAMS_DIR)

    def get_team_param(self):
        """Generates a .json with a all team info, where the teamID acts as key.
        season_params must have been generated as it looks for it to load seasonIDs.
        Adds all the seasons the team has played in in a list with league
        abbreviation as key.
        """

        #Gets the league abbreviations from fb_league
        teams = {}
        #loads league and their seasons from season_params.json
        league_season_info = self.dir.load_json('season_params.json', StorageConfig.PARAMS_DIR)
        #Iterates over league-season in league_season_info
        for league, season in tqdm(league_season_info.items()):
            seasons = self.fb.leagues[str(league)].load_seasons()
            #Iterates over season_label and ID in seasons
            for season_label, season_id in seasons.items():
                #Gets teams for a specific season
                league_teams = self.fb.leagues[str(league)].seasons[str(season_label)].load_teams()
                #Separates the team_id from it's values
                for team, val in league_teams.items():
                    #Adds the team_id and it's values if not in teams
                    if team not in teams:
                        teams.update({team:val})
                        #Add championship key to new teams
                        teams[team].update({'championships':{league:[]}})
                        teams[team]['championships'][league].append(str(season_label))

                        #If season_id matches the season_id in team values
                        #and the league exist as key in championships it appends the seasonID
                    elif season_id['id'] == val['competition'] and league in teams[team]['championships']: 
                        teams[team]['championships'][league].append(str(season_label))

                        #If season_id matches the season_id in team values and the league doesn't exist
                        #as key in championships it adds the league as key and appends the seasonID
                    elif season_id['id'] == val['competition'] and league not in teams[team]['championships']:
                        teams[team]['championships'][league] = []
                        teams[team]['championships'][league].append(str(season_label))
        self.dir.save_json('teams_params', teams, StorageConfig.PARAMS_DIR)

def main():
    """Runs the script to 
    get the .json param files"""
    d = Params()
    print('Retrieving leagues..')
    d.league_param()
    print('Retrieving league-seasons..')
    d.league_season_param()
    print('Retrieving teams..')
    d.get_team_param()
    print('Finished')

if __name__ == '__main__':
    main()