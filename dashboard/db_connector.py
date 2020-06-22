import os

import json
import pandas as pd

from pprint import pprint

from pymongo import MongoClient


class DBConnector:

    def __init__(self, league, season):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majorit'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[self.league + self.season]
        self.collections = self.DATABASE.collection_names()

    def collection_names(self):
        return self.collections


class Collections(DBConnector):   
    def __init__(self, league, season):
        DBConnector.__init__(self, league, season)
        collections = {collection: self.DATABASE[collection]
                                for collection in self.collection_names()}
        self.__dict__.update(collections)



class LeagueDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.league_standings

    def get_league_teams(self):
        return self.collection.distinct('team_shortName')

    def get_league_standings_overall(self):
        return self.collection.find(
            {},
            {
            "team_shortName": 1,
            "position": 1,
            "overall_played": 1,
            "overall_won": 1,
            "overall_draw": 1,
            "overall_lost": 1,
            "overall_goalsFor": 1,
            "overall_goalsAgainst": 1,
            "overall_goalsDifference": 1,
            "overall_points": 82,
            "_id": 0,
            })

class PlayersDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.player_stats

class FixturesDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.fixture_stats

    def get_fixtures(self):
        return self.collection.find({ "id": { "$exists": "true" } })

class TeamsDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.team_standings











if __name__ == '__main__':

    for i in FixturesDB('EN_PR', '2019').get_fixtures():
        print(i)
