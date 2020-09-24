import datetime
import multiprocessing
import os
import pymongo
import sys
import time
import types
import uuid


from bson.objectid import ObjectId
from directory import Directory
from multiprocessing import Pool
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import MongoClient
from storage_config import StorageConfig
from tqdm import tqdm

dir = Directory()

def DB_collections(collection_type):
    types = {'p': 'player_stats',
             't': 'team_standings',
             'f': 'fixture_stats',
             'l': 'league_standings',
             'pf': 'fixture_players_stats'}
    return types.get(collection_type)



class DB():

    def __init__(self, league, season, func=None):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[league + season]

        self.league = league
        self.season = season

        self.pool = multiprocessing.cpu_count()
        self.playerfile = self.league + '_' + self.season + '_playerstats.json'
        self.teamfile = self.league + '_' + self.season + '_team_standings.json'
        self.fixturefile = self.league + '_' + self.season + '_fixturestats.json'
        self.leaguefile = self.league + '_' + self.season + '_league_standings.json'
        self.player_fixture = self.league + '_' + self.season + '_player_fixture.json'
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
        print("Please check that", file, "exists")

def check_record(collection, index_dict):
    """Check if record exists in collection
        Args:
            index_dict (dict): key, value
    """
    return collection.find_one(index_dict)

def collection_index(collection, index, *args):
    """Checks if index exists for collection, 
    and return a new index if not

        Args:
            collection (str): Name of collection in database
            index (str): Dict key to be used as an index
            args (str): Additional dict keys to create compound indexs
    """
    compound_index = tuple((arg, ASCENDING) for arg in args)
    if index not in collection.index_information():
        return collection.create_index([(index, DESCENDING), *compound_index], unique=True)

def push_upstream(collection, record):
    """Update record in collection
        Args:
            collection (str): Name of collection in database
            record_id (str): record _id to be put for record in collection
            record (dict): Data to be pushed in collection
    """
    return collection.insert_one(record)

def update_upstream(collection, index_dict, record):
    """Update record in collection
        Args:
            collection (str): Name of collection in database
            index_dict (dict): key, value
            record (dict): Data to be updated in collection
    """
    return collection.update_one(index_dict, {"$set": record}, upsert=True)

def executePushPlayer(db):

    playerstats = load_file(db.playerfile)
    collection_name = DB_collections('p')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'p_id')
    for player in tqdm(playerstats):
        existingPost = check_record(collection, {'p_id': player['p_id']})
        if existingPost:
            update_upstream(collection, {'p_id': player['p_id']}, player)
        else:
            push_upstream(collection, player)


def executePushFixture(db):

    fixturestats = load_file(db.fixturefile)
    collection_name = DB_collections('f')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id')
    for fixture in tqdm(fixturestats):
        existingPost = check_record(collection, {'f_id': fixture['f_id']})
        if existingPost:
            update_upstream(collection, {'f_id': fixture['f_id']}, fixture)
        else:
            push_upstream(collection, fixture)

def executePushTeam(db):

    team_standings = load_file(db.teamfile)
    collection_name = DB_collections('t')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_shortName', 'played')
    for team in tqdm(team_standings):
        existingPost = check_record(collection, {'team_shortName': team['team_shortName'],
                                                 'played': team['played']})
        if existingPost:
            update_upstream(collection, {'team_shortName': team['team_shortName'],
                                        'played': team['played']}, team)
        else:
            push_upstream(collection, team)

def executePushLeagueStandings(db):

    league_standings = load_file(db.leaguefile)
    collection_name = DB_collections('l')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_shortName')
    for team in tqdm(league_standings):
        existingPost = check_record(collection, {'team_shortName': team['team_shortName']})
        if existingPost:
            update_upstream(collection, {'team_shortName': team['team_shortName']}, team)
        else:
            push_upstream(collection, team)

def executePushFixturePlayerStats(db):

    player_fixture = load_file(db.player_fixture)
    collection_name = DB_collections('pf')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id', 'id')
    for player in tqdm(player_fixture):
        existingPost = check_record(collection, {'f_id': player['f_id'],
                                                 'id': player['id']})
        if existingPost:
            update_upstream(collection, {'f_id': player['f_id'],
                                        'id': player['id']}, player)
        else:
            push_upstream(collection, player)     

if __name__ == '__main__':
    db = DB('EN_PR', '2019')
    player_fixture = load_file(db.player_fixture)
    for i in player_fixture:
        print(i['f_id'])
    # print(os.environ.get('DB_user'))
    # en_pr2019 = DB('EN_PR', '2019')
    # executePushPlayer(en_pr2019)
    # executePushFixture(en_pr2019)
    # executePushTeam(en_pr2019)
    # en_pr2018 = DB('EN_PR', '2018')
    # executePushPlayer(en_pr2018)
    # executePushFixture(en_pr2018)
    # executePushTeam(en_pr2018)


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

