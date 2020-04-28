"""Checks if all needed information exist on api for a league by season.

Input: A leagueID to check

Output: Console output with True/False values if information exist

**How the class checks if data exists**:

User provides a known leagueID, a request is made with the ID to see which seasons
exist. 
If no seasonIDs exist, it stops else takes all the seasonIDs and stores them.
For each seasonID it checks if fixtures exists, if it exists it stores them and
uses them to see if fixture stats exists. 
If fixture stats exist it requests att teams in 

"""
from directory import Directory
from directory import StorageConfig
from api_scraper import Football
import requests
from tqdm import tqdm
from pprint import pprint
import sys



class ValidateParams():
    dir = Directory()
    fb = Football()

    def __init__(self, league_file='league_params.json', team_seasons_file='teams_params.json' ):
        self.leagues = self.import_id(league_file)
        self.team_seasons = self.import_id(team_seasons_file)
        self.league_file = league_file

    def import_id(self, file):
        """Imports a json file in read mode
            
            Args:
                file(str): Name of file
        """
        return self.dir.load_json(file , StorageConfig.PARAMS_DIR)

    def make_request(self, url):
        """Makes a GET request

            Args:
                url (str): url to webbsite
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        params = (('pageSize', '100'),)           
        response = requests.get(url, params = params, headers=headers)
        return response.status_code

    def check_current_season(self):
        """
         Checks if request gives response code 200
        """
        failed = {}
        league = self.leagues
        print('Checking leagues..')
        for league_name, league_id in tqdm(league.items()):
            status = self.make_request(f'https://footballapi.pulselive.com/football/competitions/{league_id}/compseasons/current')
            if status != 200:
                failed.update({league_name:league_id})
        print(failed)
        return failed

    def remove_failed_leagues(self, failed_leagues):
        """Removes failed leagues from .json file

            Args:
                failed_leagues (dict): dict with leagues existing in initial file
        """
        league = self.import_id('season_params.json')
        deleted = []
        print('Deleting failed leagues..')
        for failed in failed_leagues.keys():
            if failed in league:
                del league[failed]
                deleted.append(failed)
        print("Below leagues have been removed from", self.league_file)       
        print("\n".join(deleted))
        self.dir.save_json('season_params', league, StorageConfig.PARAMS_DIR)

    def check_stats_urls(self):
        failed = {}
        self.fb.load_leagues()
        #loads league and their seasons from season_params.json
        league_season_info = self.dir.load_json('season_params.json', StorageConfig.PARAMS_DIR)
        #Iterates over league-season in league_season_info
        for league, season in league_season_info.items():
            seasons = self.fb.leagues[str(league)].load_seasons()
            #Iterates over season_label and ID in seasons
            for season_label, season_id in seasons.items():
                s_id = season_id['id']
                #Gets teams for a specific season
                league_teams = self.fb.leagues[str(league)].seasons[str(season_label)].load_teams()
                for team in league_teams.keys():
                    status = self.make_request(
                        f'https://footballapi.pulselive.com/football/teams/{team}/compseasons/{s_id}/staff')
                if status != 200 and league not in failed:
                   failed.update({s_id:league})
        print(failed)
        return failed




    def main(self):
        return self.remove_failed_leagues(self.check_current_season())

if __name__ == '__main__':
    ValidateParams().main()
    # def make_request(url):
    #     """Makes a GET request

    #         Args:
    #             url (str): url to webbsite
    #     """
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #                         'Origin': 'https://www.premierleague.com',
    #                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    #               }
    #     params = (('pageSize', '100'),)           
    #     response = requests.get(url, params = params, headers=headers)
    #     return response.status_code

    # status = make_request(
    #     'https://footballapi.pulselive.com/football/teams/131/compseasons/1/staff?page=0&pageSize=100')
    # print(status)
    #d = ValidateParams()
    #d.remove_failed_leagues(d.check_current_season())
    #d.main()



