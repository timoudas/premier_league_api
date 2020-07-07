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

    def gk_test(self):
        return self.collection.aggregate([
            {"$match":{
                "position": "G"
                },
            },
            {"$project":{
                'total_goal_kicks': 1,
                }
            }
        ])

    def get_goalkeeper_avg_stats(self):
        """Get goalkeeper average stats"""
        prefix = 'avg_'
        return self.collection.aggregate([
            {"$match":{
                "position": "G"
                },
            },
            {"$project":{
                'total_clearance': 1,
                # prefix + 'accurate_back_zone_pass': { 
                #     '$multiply': [{'$divide': ['$accurate_back_zone_pass', '$total_back_zone_pass']}, '$appearances']
                # },
                # prefix + 'accurate_chipped_pass': { 
                #     '$multiply': [{'$divide': ['$accurate_chipped_pass', '$total_chipped_pass']}, '$appearances']
                # },
                # prefix + 'accurate_fwd_zone_pass': { 
                #     '$multiply': [{'$divide': ['$accurate_fwd_zone_pass', '$total_fwd_zone_pass']}, '$appearances']
                # },
                # prefix + 'accurate_goal_kicks': { 
                #     '$multiply': [{'$divide': ['$accurate_goal_kicks', '$goal_kicks']}, '$appearances']
                # },
                # prefix + 'accurate_keeper_throws': { 
                #     '$multiply': [{'$divide': ['$accurate_keeper_throws', '$keeper_throws']}, '$appearances']
                # },
                # prefix + 'accurate_long_balls': { 
                #     '$multiply': [{'$divide': ['$accurate_long_balls', '$total_long_balls']}, '$appearances']
                # },
                # prefix + 'accurate_pass': { 
                #     '$multiply': [{'$divide': ['$accurate_pass', '$total_pass']}, '$appearances']
                # },
                # prefix + 'effective_clearance': { 
                #     '$multiply': [{'$divide': ['$effective_clearance', '$total_clearance']}, '$appearances']
                # },
                # prefix + 'accurate_back_zone_pass': { 
                #     '$multiply': [{'$divide': ['$final_third_entries', '$total_final_third_passes']}, '$appearances']
                # },
                # prefix + 'accurate_back_zone_pass': { 
                #     '$multiply': [{'$divide': ['$', '$total_launches']}, '$appearances']
                # },
                '_id': 0,
                'name': '$name'

                },
            },
            {'$sort': {prefix + 'accurate_back_zone_pass': -1}}

        ])

    def avg_rank_goalkeepers(self, metric, total_metric):
        prefix = 'avg_'
        return self.collection.aggregate([
            {
                "$match":{
                    "position": "G"
                },
            },
            {
                "$project":{
                    'accurate_back_zone_pass': { 
                        '$multiply': [{'$divide': ['$' + metric, '$' + total_metric]}, '$appearances']
                    },
                'name': '$name',
                '_id': 0,
                },
            },
            {
                '$sort': {
                    'accurate_back_zone_pass': -1
                }
            }
        ])


class FixturesDB(Collections):
    def __init__(self, league, season):
        Collections.__init__(self, league, season)
        self.collection = self.fixture_stats

    def get_fixtures(self):
        return self.collection.find({ "id": { "$exists": "true" } })

    def get_fixture_events(self, fixture_id):
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
        ])

    def get_fixture_lineups(self, fixture_id):
        return self.collection.aggregate([
              {
                "$match": {
                  "f_id": 46605
                }
              },
              {
                "$unwind": "$lineUps"
              },
              {
                "$project": {
                  "_id": 0,
                  "teamId": "$lineUps.teamId",
                  "matchPosition": "$lineUps.matchPosition",
                  "id": "$lineUps.id",
                  "captain": "$lineUps.captain",
                  "playerId": "$lineUps.playerId",
                  "position": "$lineUps.position",
                  "shirtNum": "$lineUps.shirtNum",
                  "positionInfo": "$lineUps.positionInfo",
                  "name": "$lineUps.name",
                  "first": "$lineUps.first",
                  
                }
              }
            ])

    def get_fixture_substitutes(self, fixture_id):
        return self.collection.aggregate([
            {
                "$match": {
                  "f_id": 46605
                }
            },
            {
                "$unwind": "$substitutes"
            },
            {
                "$project": {
                      "_id": 0,
                      "teamId": "$substitutes.teamId",
                      "matchPosition": "$substitutes.matchPosition",
                      "id": "$substitutes.id",
                      "captain": "$substitutes.captain",
                      "playerId": "$substitutes.playerId",
                      "position": "$substitutes.position",
                      "shirtNum": "$substitutes.shirtNum",
                      "positionInfo": "$substitutes.positionInfo",
                      "name": "$substitutes.name",
                      "first": "$substitutes.first",
                  
                }
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
    metric_tuple = [
        ('accurate_back_zone_pass', 'total_back_zone_pass'),
        ('accurate_chipped_pass', 'total_chipped_pass'),
        ('accurate_fwd_zone_pass', 'total_fwd_zone_pass'),
        ('accurate_goal_kicks', 'goal_kicks'), #goal_kicks: total_goal_kicks
        ('accurate_keeper_sweeper', 'total_keeper_sweeper'),
        ('accurate_keeper_throws', 'keeper_throws'), #keeper_throws: total_keeper_throws
        ('accurate_launches', 'total_launches'),
        ('accurate_long_balls', 'total_long_balls'),
        ('accurate_pass', 'total_pass'),
        # ('aerial_lost', 'aerial_lost + aerial_won') #total_aerial: 'aerial_lost + aerial_won'
        # ('aerial_won', 'aerial_lost + aerial_won')
        # ('attempts_conceded_ibox', 'attempts_conceded_ibox + attempts_conceded_obox') #total_attempts_conceded: 'attempts_conceded_ibox + attempts_conceded_obox'
        # ('attempts_conceded_obox', 'attempts_conceded_ibox + attempts_conceded_obox')
        ('goals_conceded_ibox', 'goals_conceded'), #total_goals_coneded: goals_conceded
        ('goals_conceded_obox', 'goals_conceded'),
        ('', 'total_contest')





    ]
    results = PlayersDB('EN_PR', '2019').gk_test()
    df = pd.DataFrame(results)
    print(df)

