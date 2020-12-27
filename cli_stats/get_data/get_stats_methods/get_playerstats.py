from .helper_methods import Base
from .helper_methods import load_match_data
from storage_config import StorageConfig
from multiprocessing import Pool
import requests
import re
from tqdm import tqdm

class PlayerStats(Base):

    def __init__(self, *args, **kwargs):
        """Player IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.player_dispatch_map = {'player_stats' : self.player_stats}


    def load_season_players(self):
        """
        Loads the playerIds into a list for a given league-season. 
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} players')
        player_id_temp = []
        for team in tqdm(self.teams.values()):
            try:
                players = self.fb.leagues[self.league].seasons[self.season].teams[team['shortName']].load_players()
            except:
                print(f"Something weong with connection to {self.league} {self.season} {team}")
            if players:
                for player in players.keys():
                    player_id_temp.append(player)
            else:
                print(f"Found no players for {self.league} {self.season} {team}")
        player_id_tup = set(player_id_temp)
        player_id = list(player_id_tup)          
        print('Initialization completed')
        return player_id


    def player_stats_singel(self, player):
        """Returns a a json-response for player stats"""
        
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/stats/player/{player}?compSeasons={self.season_id}')
        return ds

    def player_stats(self):
        """Gets stats for all players in a league-season using multithreading
        saves output in a json file.
         """
        player_ids = self.load_season_players()
        stats_list = []
        print("Getting player stats..")
        with Pool(self.pool) as p:
            player_stats = list(tqdm(p.imap(self.player_stats_singel, player_ids), total=len(player_ids)))
        print('Getting data from workers..')
        all_players = player_stats
        i = 0
        for player in all_players:
            stats = {"info": {}}
            stats["info"] = player['entity']
            stats['info'].update({'seasonId': self.season_id,
                                    'seasonLabel': self.season_label})
            if player['stats']:
                stats['stats'] = player['stats']
                stats['stats'].append({'id':player['entity']['id']})
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} players retreived had no stats')
        self.save_completed('playerstats', stats_list, StorageConfig.STATS_DIR)

if __name__ == '__main__':
	PlayerStats()