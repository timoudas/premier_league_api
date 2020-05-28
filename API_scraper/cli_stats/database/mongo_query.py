import os

import pandas as pd

from pprint import pprint

from pymongo import MongoClient

class DB():

    def __init__(self, league, season):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@database-mbqxj.mongodb.net/test?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client["Database"]
        self.collection = self.DATABASE[self.league + self.season]

    
    def get_fixtures(self):
        return self.collection.find({ "f_id": { "$exists": "true" } })

    def get_players(self):
        return self.collection.find({ "p_id": { "$exists": "true" } })

    def get_teams_standing(self):
        return self.collection.find({ "t_id": { "$exists": "true" } })


    def get_position(self, position):
        return self.collection.find(
            { "position": position},
            )


if __name__ == '__main__':
    test = DB('EN_PR', '2018')
    query = test.get_fixtures()
    df = pd.DataFrame.from_dict(query)
    print(df)
