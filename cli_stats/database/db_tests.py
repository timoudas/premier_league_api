import os
import pymongo

class DBConn():

    def __init__(self, DB_NAME='PremierLeague'):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[DB_NAME]
