import os

import json
import pandas as pd

from pprint import pprint

from pymongo import MongoClient


class DBConnector:

    def __init__(self, league, season):
        self.db_user = "Timoudas"
        self.db_pass = "adde123"
        #self.db_user = os.environ.get('DB_user')
        #self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/EN_PR2019?authSource=admin'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[self.league + self.season]
        self.collections = self.DATABASE.list_collection_names()

    def collection_names(self):
        return self.collections

    def find(self, query_dict=None, fields=None, limit=0):
      """Returns a custom query on a collection"""
      return self.collection.find(query_dict, fields).limit(limit)
    
    def aggregate(self, pipeline):
      """Returns an aggregation"""
      return self.collection.aggregate(pipeline)


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

    def get_fixture_events(self, fixture_id, limit=5):
        return self.collection.aggregate([
            {"$match": 
            {"f_id": fixture_id}
            },
            {"$unwind": "$events"},

            {
            "$project": {
                "_id": 0,
                'Type': "$events.types", 
                'HS': "$events.awayScore", 
                'AS': '$events.homeScore',
                'Phase': '$events.phase',
                'clockLabel': '$fixtures.clockLabel',
                'Id': "$events.id"
                }
            },
            {
              '$limit': limit
            }

        ])

class TeamsDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.team_standings

    def get_latest_fixtures(self, team_shortName, limit=5):
        """Get the latest fixtures for a team
            Args:
                team_shortName (str): A teams shortname
                limit (int): Total number of documents to retrieve

        """
        return self.collection.aggregate([
            {"$match": 
                {"team_shortName": team_shortName}
            },
            {"$sort": {"gameweek": -1}},
            {"$unwind": "$fixtures"},

            {
            "$project": {
                "_id": 0,
                'HTeam': "$fixtures.home_team_shortName", 
                'ATeam': "$fixtures.away_team_shortName", 
                'H': '$fixtures.home_team_score',
                'A': '$fixtures.away_team_score',
                'G': '$fixtures.gameweek',
                'Id': "$fixtures.f_id"
                }
            },
            {
            "$limit": limit
            }
            ])


if __name__ == '__main__':
    results = FixturesDB('EN_PR', '2019').get_fixture_events(46605)
    for i in results:
      pprint(i)

