from .helper_methods import Base
from .helper_methods import load_match_data
from storage_config import StorageConfig
from multiprocessing import Pool
import requests
import re
from tqdm import tqdm

class FixtureStats(Base):

    def __init__(self, *args, **kwargs):
        """Fixture IDs are loaded into a list from method within the class.
        That is so that they don't have to be created everytime that they are needed, and 
        save time."""
        Base.__init__(self, *args, **kwargs)
        self.fixture_ids = [fix['id'] for fix in self.load_season_fixture().values()]
        self.fixture_dispatch_map = {'fixture_player_stats': self.fixture_player_stats,
                                     'fixture_stats' : self.fixture_stats,
                                     'fixture_info': self.fixture_info,}



    def load_season_fixture(self):
        """Loads the fixtures for a league-season,
        calls api_scraper.py methods
        """

        print(f'Initializing \t {self.league} \t {self.season} fixtures')
        print('Initialization completed')
        return self.fb.leagues[self.league].seasons[self.season].load_played_fixtures()

    def fixture_stats_singel(self, fixture):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/stats/match/{fixture}')
        return ds

    def fixture_stats(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats_list = []
        print("Getting fixture stats..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for fixture in fixture_stats:
            stats = {}
            stats['info'] = fixture['entity']
            if 'data' in fixture:
                stats['stats'] = fixture['data']
            else:
                i += 1
            if stats:
                stats_list.append(stats)

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('fixturestats', stats_list, StorageConfig.STATS_DIR)

    def fixture_info_singel(self, fixture_id):
        """Gets stats for a fixture"""
        ds = load_match_data(f'https://footballapi.pulselive.com/football/fixtures/{fixture_id}')
        return ds

    def fixture_info(self):
        """Gets stats for all fixtures in a league-season using multithreading
        saves output in a json file.

        """
        stats_list = []
        print("Getting fixture info..")
        with Pool(self.pool) as p:
            fixture_info = list(tqdm(p.imap(self.fixture_info_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for info in fixture_info:
            stats = {}
            if info:
                stats = info
            else:
                i += 1
            if stats:
                stats_list.append(stats)

        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('fixtureinfo', stats_list, StorageConfig.STATS_DIR)


    def fixture_player_stats_singel(self, fixture_id, player_id):
        """Gets stats a player for a fixture"""
        fixture = load_match_data(f'https://footballapi.pulselive.com/football/stats/player/{player_id}?fixtures={fixture_id}')
        i = 0
        stats = {}
        if 'entity' in fixture:
            stats['info'] = fixture['entity']
            stats['info'].update({'f_id': fixture_id, 
                                    'seasonId':self.season_id,
                                    'seasonLabel': self.season_label})
        else:
            print(f'Could not get info on: f_id:{fixture_id}, p_id{player_id}')
        if 'stats' in fixture:
            stats['stats'] = fixture['stats']
            stats['stats'].append({'id':fixture['entity']['id']})
        else:
            i += 1
        if stats:
            return stats

    def fixture_player_stats_singel_wrapper(self, params):
        """Wrapper to pass tuple args to multiprocess"""
        return self.fixture_player_stats_singel(*params)

    
    def load_fixture_player_stats(self):
        """Loads all the players for each fixture"""
        stats_list = []

        print("Getting fixture players..")
        with Pool(self.pool) as p:
            fixture_info = list(tqdm(p.imap(self.fixture_info_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))
        print('Getting data from workers..')
        i = 0
        for info in fixture_info:
            stats = {}
            if info:
                stats = {info['id']: []}
            if 'teamLists' in info:
                team_list = info['teamLists']
                for lineups in team_list:
                    if lineups:
                        team_id = lineups['teamId']
                        lineup = lineups['lineup']
                        substitutes = lineups['substitutes']
                        for l in lineup:
                            stats[info['id']].append(l['id'])
                        for s in substitutes:
                            stats[info['id']].append(s['id'])
            else:
                i += 1
            if stats:
                stats_list.append(stats)
        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        return stats_list

    def fixture_player_stats(self):
        """Create a list of tuples (fixture_id, player_id) to pass to the
        multiprocess for speed. Only create tuple of games that has been played.

        """
        stats_list = []
        fixture_tuples = []
        fixture_player_ids = self.load_fixture_player_stats()
        i = 0
        for fixture in fixture_player_ids:
            for fixture_id, value in fixture.items():
                if value:
                    for player_id in value:
                        fixture_tuples.append((fixture_id, player_id))
        print("Getting player info for all fixtures..")
        with Pool(self.pool) as p:
            fixture_stats = list(tqdm(p.imap(self.fixture_player_stats_singel_wrapper, fixture_tuples, chunksize=1), total=len(fixture_tuples)))
            for fixture in fixture_stats:
                if fixture:
                    stats_list.append(fixture)
                else:
                    i += 1
        print('Completed')
        if i >0:
            print(f'{i} games retreived had no stats')
        self.save_completed('player_fixture', stats_list, StorageConfig.STATS_DIR)