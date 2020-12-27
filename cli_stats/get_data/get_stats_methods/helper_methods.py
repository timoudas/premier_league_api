import multiprocessing
import requests
import re

from ..api_scraper.api_scraper import Football #
from .static_types import * #
from directory import Directory
from multiprocessing import Pool
from storage_config import StorageConfig


#Global session for speed
session = requests.Session()


def load_match_data(url):
    """Retreives Ids for different pages on the API"""
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
              }
    params = (('pageSize', '100'),)
    # request to obtain the team info
    try:
        response = session.get(url, headers=headers, params=params).json()
        return response
    except Exception as e:
        print(e, 'Something went wrong with the request')
        return {}

class Base():
    fb = Football()
    dir = Directory()


    def __init__(self, league, season):
        """Initiates the class by counting the cores for later multiprocessing.

            Args:
                league(str): A league in the form of it's abbreviation. Ex. 'EN_PR'
                season(str): A season that exists for that specific league EX. '2019/2020'
        """
        if season:
            if re.match(r"(^\d{4})([/]\d{4}$)", season): #YYYYMMDDTHHMMSS
                self.season = season
            else: #YYYY
                self.season = f'{season}/{str(int(season)+1)}'
        self.pool = multiprocessing.cpu_count()
        self.league = league
        self.season_label = f'{self.season[:5]}/{str(int(self.season[5:7])+1)}'
        self.fb.load_leagues()
        self.fb.leagues[self.league].load_seasons()
        self.season_id = self.fb.leagues[self.league].seasons[self.season]['id']
        self.teams = self.fb.leagues[self.league].seasons[self.season].load_teams()
        self.year = re.search( r'(\d{4})', self.season).group()
        self.league_season = f'{self.league}_{self.year}'



    def save_completed(self, filename, stats_list, path):
        """Saves dict to json file.

        Args:
            filename(str): The name of the file
            stats_list(list of dicts): The content that is to be saved
            path(str): The path to were the content is to be saved

        """
        filename = f'{self.league_season}_{filename}'
        self.dir.save_json(filename, stats_list, path)
        print(f'Saved as {filename}.json in {path}')

if __name__ == '__main__':
	pass