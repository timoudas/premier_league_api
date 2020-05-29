import cmd 
import os
import pickle
import sys

from bson.objectid import ObjectId
from docopt import DocoptExit
from docopt import docopt
from pprint import pprint

sys.path.insert(0, '../directory')
sys.path.insert(0, '../database')


from directory import StorageConfig
from mongo_db import DB
from mongo_db import Directory

dir = Directory()

def load_stats(league, season, stats_type):
    file = f'{league}_{season}_{stats_type}.json'
    data = dir.load_json(file, StorageConfig.DB_DIR)
    return data

def check_len_fixture(league, season):
    data = load_stats(league, season, 'fixturestats')
    records = len(data)
    print(f'Total records in {league}\t{season} fixturestats:', records)

def check_len_team(league, season):
    data = load_stats(league, season, 'playerstats')
    records = len(data)
    print(f'Total records in {league}\t{season} playerstats:', records)

def check_len_player(league, season):
    data = load_stats(league, season, 'team_standings')
    records = len(data)
    print(f'Total records in {league}\t{season} team_standings:', records)



def check_db_records(league, season):
    data = load_stats(league, season, 'playerstats')
    for d in data:
        print(d['id'])
    data = load_stats(league, season, 'fixturestats')
    for d in data:
        print(d['id'])
    data = load_stats(league, season, 'team_standings')
    for d in data:
        print(d['id'])
    

def key_length(league, season):
    data = load_stats(league, season, 'playerstats')
    count = 0
    good = 0
    for d in data:
        if d['id']:
            count +=1
        else:
            good += 1
    print("count", count)
    print("good", good)

def check_id(league, season):
    data = load_stats(league, season, 'playerstats')
    count = 0
    for d in data:
        if d.get('id') != None:
            count += 1
    print(count)


# check_len_fixture('EN_PR', '2018')
# check_len_player('EN_PR', '2018')
# check_len_team('EN_PR', '2018')
# check_db_records('EN_PR', '2018')
check_len_fixture('EN_PR', 2018)