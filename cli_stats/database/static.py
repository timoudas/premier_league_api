from directory import Directory
from storage_config import StorageConfig
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import UpdateOne

dirs = Directory()

def DB_collections(collection_type):
    types = {'p': 'player_stats',
             't': 'team_standings',
             'f': 'fixture_stats',
             'l': 'league_standings',
             'pf': 'fixture_players_stats',
             's': 'team_squads'}
    return types.get(collection_type)

def import_json(file):
    """Imports a json file in read mode
        Args:
            file(str): Name of file
    """
    return dirs.load_json(file , StorageConfig.DB_DIR)

def load_file(file):
    try:
        loaded_file = import_json(file)
        return loaded_file
    except FileNotFoundError:
        print("Please check that", file, "exists")


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

def update_upstream(index_dict, record):
    """Update record in collection
        Args:
            index_dict (dict): key, value
            record (dict): Data to be updated in collection
    """
    return UpdateOne(index_dict, {"$set": record}, upsert=True)
