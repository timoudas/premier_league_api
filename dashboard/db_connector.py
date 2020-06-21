import os

import pandas as pd

from pprint import pprint

from pymongo import MongoClient


class DBConnector:

    def __init__(self, league, season):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majorit'
        self.client = MongoClient(self.MONGODB_URL)
        self.database = self.client[self.league + self.season]
        self.collections = self.database.collection_names()

class LeagueDB(DBConnector):
    def __init__(self, *args, **kwargs):
        DBConnector.__init__(*args, **kwargs)
        self.collection = 'league_standings'

class PlayersDB(DBConnector):
    def __init__(self, *args, **kwargs):
        DBConnector.__init__(*args, **kwargs)
        self.collection = 'player_stats'

class FixturesDB(DBConnector):
    def __init__(self, *args, **kwargs):
        DBConnector.__init__(*args, **kwargs)
        self.collection = 'fixture_stats'

class TeamsDB(DBConnector):
    def __init__(self, *args, **kwargs):
        DBConnector.__init__(*args, **kwargs)
        self.collection = 'team_standings'

class Query(LeagueDB, TeamsDB):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test():
        

    def get_standings(self):
        query = self.collection.find(
            {"t_id": { "$exists": "true" }},
            {
            "team_shortName": 1,
            "gameweek": 1,
            "points": 1,
            "played": 1,
            "_id": 0,
            })
        return query






if __name__ == '__main__':

    print(Query('EN_PR', '2019').get_standing())

