import multiprocessing
import os
import pymongo

from pprint import pprint

from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import MongoClient
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from .static import DB_collections, load_file, collection_index, update_upstream

class DB():

    def __init__(self, league, season, func=None):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.league = league
        self.season = str(season)
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[self.league + self.season]


        self.pool = multiprocessing.cpu_count()
        self.playerfile = f'{self.league}_{self.season}_playerstats.json'
        self.teamfile = f'{self.league}_{self.season}_team_standings.json'
        self.fixturefile = f'{self.league}_{self.season}_fixturestats.json'
        self.leaguefile = f'{self.league}_{self.season}_league_standings.json'
        self.player_fixture = f'{self.league}_{self.season}_player_fixture.json'
        self.func = func

    def execute(self):
        if self.func is not None:
            return self.func(self)

def executePushPlayer(db):
    updates = []
    playerstats = load_file(db.playerfile)
    collection_name = DB_collections('p')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'p_id')
    print(f'Pushing updates to:  {collection_name}')
    for player in playerstats:
        updates.append(update_upstream({'p_id': player['p_id']}, player))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushFixture(db):
    updates = []
    fixturestats = load_file(db.fixturefile)
    collection_name = DB_collections('f')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id')
    print(f'Pushing updates to:  {collection_name}')
    for fixture in fixturestats:
        updates.append(update_upstream({'f_id': fixture['f_id']}, fixture))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushTeam(db):
    updates = []
    team_standings = load_file(db.teamfile)
    collection_name = DB_collections('t')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_shortName', 'played')
    print(f'Pushing updates to:  {collection_name}')
    for team in team_standings:
        updates.append(update_upstream({'team_shortName': team['team_shortName'],
                                        'played': team['played']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushLeagueStandings(db):
    updates = []
    league_standings = load_file(db.leaguefile)
    collection_name = DB_collections('l')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_shortName')
    print(f'Pushing updates to:  {collection_name}')
    for team in league_standings:
        updates.append(update_upstream({'team_shortName': team['team_shortName']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushFixturePlayerStats(db):
    updates = []
    player_fixture = load_file(db.player_fixture)
    collection_name = DB_collections('pf')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id', 'id')
    print(f'Pushing updates to:  {collection_name}')
    for player in player_fixture:
        updates.append(update_upstream({'f_id': player['f_id'],
                                        'id': player['id']}, player))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')

def executePushTeamSquads(db):
    updates = []
    team_squads = load_file(db.team_squads)
    collection_name = DB_collections('s')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'teamId')
    print(f'Pushing updates to:  {collection_name}')
    for team in team_squads:
        updates.append(update_upstream({'teamId': team['teamId']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')

############### LEGACY ###################

# def update_upstream(collection, index_dict, record):
#     """Update record in collection
#         Args:
#             collection (str): Name of collection in database
#             index_dict (dict): key, value
#             record (dict): Data to be updated in collection
#     """
#     return collection.update_one(index_dict, {"$set": record}, upsert=True)

# def check_record(collection, index_dict):
#     """Check if record exists in collection
#         Args:
#             index_dict (dict): key, value
#     """
#     return collection.find_one(index_dict)

# def push_upstream(collection, record):
#     """Update record in collection
#         Args:
#             collection (str): Name of collection in database
#             record_id (str): record _id to be put for record in collection
#             record (dict): Data to be pushed in collection
#     """
#     return collection.insert_one(record)

if __name__ == '__main__':
	pass