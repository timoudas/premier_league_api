from .helper_methods import Base
from .helper_methods import load_match_data
from multiprocessing import Pool
import requests
import re
from storage_config import StorageConfig
from tqdm import tqdm

class TeamStats(Base):

    def __init__(self, *args, **kwargs):
        """Team IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.team_ids = [team['id'] for team in self.load_season_teams().values()]
        self.team_dispatch_map = {'team_standings' : self.team_standings,
                             'team_squad': self.team_squad}


    def load_season_teams(self):
        """Loads the teams for a league-season,
        calls api_scraper.py methods
        """
        print(f'Initializing \t {self.league} \t {self.season} teams')
        player_id = []
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_teams()

    def team_standings_singel(self, team_id):
        """Gets standing for a team"""
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/compseasons/{self.season_id}/standings/team/{team_id}')
        return ds

    def team_standings(self):
        """Gets standings for all teams in a league-season using multithreading
        saves output in a json file.
         """
        stats_list = []
        print("Getting team standings for: ", self.year)
        with Pool(self.pool) as p:
            team_standings = list(tqdm(p.imap(self.team_standings_singel, self.team_ids), total=len(self.team_ids)))
        print('Getting data from workers..')
        i = 0
        team_standing = team_standings
        for team in team_standing:
            stats = {"season": {}, "team": {}, "standing": {}}
            if 'compSeason' in team:
                stats['season'] = team['compSeason']
            if 'team' in team:
                stats['team'] = team['team']
            if 'entries' in team:
                entries = team['entries']
                stats['standing'] = []
                for entry in entries:
                    if 'fixtures' in entry:
                        stats['standing'].append(entry)
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} teams retreived had no standings')
        self.save_completed('teamstandings', stats_list, StorageConfig.STATS_DIR)

    def team_squad_singel(self, team_id):
        """Gets stats for a player"""
        ds = load_match_data(
            f'https://footballapi.pulselive.com/football/teams/{team_id}/compseasons/{self.season_id}/staff')
        return ds

    def team_squad(self):
        """Gets standings for all teams in a league-season using multithreading
        saves output in a json file.
         """
        stats_list = []
        print("Getting team squads..")
        with Pool(self.pool) as p:
            team_squads = list(tqdm(p.imap(self.team_squad_singel, self.team_ids), total=len(self.team_ids)))
        print('Getting data from workers..')
        i = 0
        team_squad = team_squads
        for team in team_squad:
            stats = {"season": {}, "team": {}, "officials": {}}
            if 'compSeason' in team:
                stats['season'] = team['compSeason']
            if 'team' in team:
                stats['team'] = team['team']
            if 'players' in team:
                stats['players'] = team['players']
            if 'officials' in team:
                stats['officials'] = team['officials']
            else:
                i += 1
            stats_list.append(stats)

        print('Completed')
        if i > 0:
            print(f'{i} teams retreived had no standings')
        self.save_completed('teamsquads', stats_list, StorageConfig.STATS_DIR)