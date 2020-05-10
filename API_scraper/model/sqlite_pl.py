import datetime
import uuid
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
        self.playerfile = self.league + '_' + self.season + '_playerstats.json'
        self.teamfile = self.league + self.season + 'teamstandings.json'
        self.fixture = self.league + self.season + 'fixturestats.json'
        self.func = func

    def execute(self):
        if self.func is not None:
            return self.func(self)


def import_json(file):
    """Imports a json file in read mode
        Args:
            file(str): Name of file
    """
    return dir.load_json(file , StorageConfig.DB_DIR)

def load_file(file):
    try:
        loaded_file = import_json(file)
        return loaded_file
    except FileNotFoundError:
        print("Please check that", loaded_file, "exists")

def check_record(collection, record_id):
    """Check if record exists in collection
        Args:
            record_id (str): record _id as in collection
    """
    return collection.find_one(player['id'])

def push_upstream(collection, record_id, record):
    """Update record in collection
        Args:
            collection (str): Name of collection in database
            record_id (str): record _id to be put for record in collection
            record (dict): Data to be pushed in collection
    """
    return collection.insert_one({"_id": record_id }, { "$set": record })

def update_upstream(collection, record_id, record):
    """Update record in collection
        Args:
            collection (str): Name of collection in database
            record_id (str): record _id as in collection
            record (dict): Data to be updated in collection
    """
    return collection.update({"_id": record_id }, { "$set": record }, upsert=True)

def executePushPlayer(db):
    load_file(db.playerfile)

    collection = db.DATABASE[db.league + db.season]
    for player in playerstats:
        existingPost = check_record(collection, player['id'])
        if existingPost:
            update_upstream(collection, player['id'], player)
        else:
            update_upstream(collection, player['id'], player)



        
            




    print(db.league)


def executePushFixture(db):
    print("Push some other data to DATABASE")

def executePushTeam(db):
    print("Push some other data to DATABASE")

if __name__ == '__main__':
    test = DB('EN_PR', '2019')
    executePushPlayer(test)

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

