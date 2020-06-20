import os

from pymongo import MongoClient

def DB_collections(collection_type):
    types = {'p': 'player_stats',
             't': 'team_standings',
             'f': 'fixture_stats',
             'l': 'league_standings'}
    return types.get(collection_type)

class DataBase():

    def __init__(self):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@database-mbqxj.mongodb.net/test?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.dbs = self.client.database_names() #returns a list of dbs
        self.connection = None
        self.DB_name = None

    def create_db(self, DB_name):
        """"""
        self.DB_name = DB_name
        return self.client[DB_name]

    def connect(self)
        

en_pr_2019 = CreateDB()
