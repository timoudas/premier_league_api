from .helper_methods import Base
from .helper_methods import load_match_data
from multiprocessing import Pool
import requests
import re
from tqdm import tqdm
from storage_config import StorageConfig

class LeagueStats(Base):

        def __init__(self, *args, **kwargs):
            Base.__init__(self, *args, **kwargs)
            self.league_dispatch_map = { 'league_standings' : self.league_standings}

        def league_standings(self):
            """Gets standing for a league"""
            stats_list = []
            print("Getting league standings..")
            response = load_match_data(
                f'https://footballapi.pulselive.com/football/standings?compSeasons={self.season_id}')
            season_info = response['compSeason']
            stats = response['tables'][0]['entries']
            for standing in stats:
                standing['seasonLabel'] = season_info['label']
                standing['seasonId'] = season_info['id']
                stats_list.append(standing)
            print('Completed')
            self.save_completed('league_standings', stats_list, StorageConfig.STATS_DIR)