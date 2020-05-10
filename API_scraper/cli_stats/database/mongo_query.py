import os

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

    def aggregate(self):
        return self.collection.aggregate([
            { "$match": { "season_id": 274} },
            { "$group": { "_id": "$team_id", "total": { "$sum": "$points" } } }
            ])

if __name__ == '__main__':
    test = DB('EN_PR', '2019')
    query = test.aggregate()
    for result_object in query:
        print(result_object)
