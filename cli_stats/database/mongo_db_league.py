import multiprocessing
import os
import pymongo

from pprint import pprint
from pymongo import ReplaceOne

from .get_schedule import get_schedule
from .static import DB_collections
from .static import collection_index
from .static import load_file
from .static import update_upstream
from pymongo import MongoClient
from pymongo.errors import BulkWriteError


class DBLeague():

    def __init__(self, league, season, func=None, DB_NAME='PremierLeague'):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.league = league
        self.season = str(season)
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[DB_NAME]


        self.pool = multiprocessing.cpu_count()
        self.playerfile = f'{self.league}_{self.season}_playerstats.json'
        self.teamfile = f'{self.league}_{self.season}_team_standings.json'
        self.fixturefile = f'{self.league}_{self.season}_fixturestats.json'
        self.leaguefile = f'{self.league}_{self.season}_league_standings.json'
        self.player_fixture = f'{self.league}_{self.season}_player_fixture.json'
        self.team_squads = f'{self.league}_{self.season}_team_squads.json'
        self.func = func

    def execute(self):
        if self.func is not None:
            return self.func(self)

def executePushPlayerLeague(db):
    updates = []
    playerstats = load_file(db.playerfile)
    collection_name = DB_collections('p')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'p_id', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for player in playerstats:
        updates.append(update_upstream({'p_id': player['p_id'],
                                        'seasonId': player['seasonId']}, player))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')

def executePushFixtureLeague(db):
    updates = []
    fixturestats = load_file(db.fixturefile)
    collection_name = DB_collections('f')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for fixture in fixturestats:
        updates.append(update_upstream({'f_id': fixture['f_id'],
        								'seasonId': fixture['seasonId']}, fixture))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushTeamLeague(db):
    updates = []
    team_standings = load_file(db.teamfile)
    collection_name = DB_collections('t')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_shortName', 'played', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for team in team_standings:
        updates.append(update_upstream({'team_shortName': team['team_shortName'],
                                        'played': team['played'],
                                        'seasonId': team['seasonId']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushLeagueStandingsLeague(db):
    updates = []
    league_standings = load_file(db.leaguefile)
    collection_name = DB_collections('l')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'team_id', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for team in league_standings:
        updates.append(update_upstream({'team_id': team['team_id'],
        								'seasonId': team['seasonId']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')


def executePushFixturePlayerStatsLeague(db):
    updates = []
    player_fixture = load_file(db.player_fixture)
    collection_name = DB_collections('pf')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'f_id', 'id', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for player in player_fixture:
        updates.append(update_upstream({'f_id': player['f_id'],
                                        'id': player['id'],
                                        'seasonId': player['seasonId']}, player))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')

def executePushTeamSquadsLeague(db):
    updates = []
    team_squads = load_file(db.team_squads)
    collection_name = DB_collections('s')
    collection = db.DATABASE[collection_name]
    collection_index(collection, 'teamId', 'seasonId')
    print(f'Pushing updates to:  {collection_name}')
    for team in team_squads:
        updates.append(update_upstream({'teamId': team['teamId'],
        								'seasonId': team['seasonId']}, team))
    try:
        collection.bulk_write(updates)
    except BulkWriteError as bwe:
        pprint(bwe.details)
    print('Done')

def executePushSchedule(db):
    updates = []
    data = get_schedule()
    collection_name = DB_collections('sc')
    collection = db.DATABASE[collection_name]
    collection.remove({})
    print(f'Pushing updates to:  {collection_name}')
    collection.bulk_write([
        ReplaceOne(
            { "id": d['id'] }, d,
            upsert=True
        )
        for d in data
    ])
    print('Done')