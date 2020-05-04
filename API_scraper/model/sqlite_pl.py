import os
from directory import Directory
from directory import StorageConfig
from pymongo import MongoClient
import clean_stats as clean
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import sys
import types

dir = Directory()


class DB():

    def __init__(self, league, season, func=None):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@database-mbqxj.mongodb.net/test?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client["Database"]
        self.league = league
        self.season = season
        self.pool = multiprocessing.cpu_count()
        self.func = func

    def execute(self):
        if self.func is not None:
            return self.func(self)

def executeReplacement1(db):
    print("Push some data to DATABASE")
    print(db.league)



def executeReplacement2(db):
    print("Push some other data to DATABASE")

if __name__ == '__main__':
    test = DB('EN_PR', '2019/2020')
    executeReplacement1(test)

# #EXAMPLE db mycol = mydb["playerstats"]
# def push_playerstats(self):
#     try:
#         stats = clean.playerstats('EN_PR', '2019')
#     except FileNotFoundError as e:
#         print("Please check that the file exists.")
#     print("Getting fixture stats..")
#     with Pool(self.pool) as p:
#         fixture_stats = list(tqdm(p.imap(self.fixture_stats_singel, self.fixture_ids, chunksize=1), total=len(self.fixture_ids)))

#     for d in stats:
#         mycol.insert_one(d)

