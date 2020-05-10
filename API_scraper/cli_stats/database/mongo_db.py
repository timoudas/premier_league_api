import datetime
import multiprocessing
import os
import sys
import types
import uuid
sys.path.insert(0, '../directory')
from directory import Directory
from directory import StorageConfig
from multiprocessing import Pool
from pymongo import MongoClient
from tqdm import tqdm

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
        self.teamfile = self.league + '_' + self.season + '_team_standings.json'
        self.fixturefile = self.league + '_' + self.season + '_fixturestats.json'
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
    return collection.find_one(record_id)

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

    playerstats = load_file(db.playerfile)
    collection = db.DATABASE[db.league + db.season]
    for player in tqdm(playerstats):
        existingPost = check_record(collection, player['id'])
        if existingPost:
            update_upstream(collection, player['id'], player)
        else:
            update_upstream(collection, player['id'], player)

def executePushFixture(db):

    fixturestats = load_file(db.fixturefile)
    collection = db.DATABASE[db.league + db.season]
    for fixture in tqdm(fixturestats):
        existingPost = check_record(collection, fixture['fixture_id'])
        if existingPost:
            update_upstream(collection, fixture['fixture_id'], fixture)
        else:
            update_upstream(collection, fixture['fixture_id'], fixture)

def executePushTeam(db):

    team_standings = load_file(db.teamfile)
    collection = db.DATABASE[db.league + db.season]
    for team in tqdm(team_standings):
        existingPost = check_record(collection, team['team_id'])
        if existingPost:
            update_upstream(collection, team['team_id'], team)
        else:
            update_upstream(collection, team['team_id'], team)

        

if __name__ == '__main__':
    test = DB('EN_PR', '2019')
    #executePushPlayer(test)
    #executePushFixture(test)
    executePushTeam(test)

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

