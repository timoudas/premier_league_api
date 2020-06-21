import os

import pandas as pd

from pprint import pprint

from pymongo import MongoClient

def DB_collections(collection_type):
    types = {'p': 'player_stats',
             't': 'team_standings',
             'f': 'fixture_stats',
             'l': 'league_standings'}
    return types.get(collection_type)

class DB():

    def __init__(self, stats_type, league, season):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majorit'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[self.league + self.season]
        self.collection = self.DATABASE[stats_type]

    
    def get_fixtures(self):
        return self.collection.find({ "f_id": { "$exists": "true" } })

    def get_players(self):
        return self.collection.find({ "p_id": { "$exists": "true" } })

    def get_teams_standing(self):
        return self.collection.find({ "t_id": { "$exists": "true" } })


    def get_position(self, position):
        return self.collection.find(
            { "position": position},
            )

    def get_teams(self):
        return self.collection.distinct('team_shortName')

    def get_standings(self):
        query = self.collection.find(
            {"t_id": { "$exists": "true" }},
            {
            "team_shortName": 1,
            "gameweek": 1,
            "points": 1,
            "played": 1,
            "_id": 0,
            })
        return query

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

    def get_standing_team_id(self, name):
        return self.collection.find(
            {'t_id': {'$exists':'true'},
            'team_shortName': {'$eq': str(name)}},
            {'_id': 0,
             't_id': 0,
             'id': 0
            }
            )
    def get_five_latest_fixture_team(self, team_shortName, limit=5):
        query = self.collection.find(
                                {"$or": [{"away_team_shortName": {'$eq': str(team_shortName)}},
                                        {"home_team_shortName": {'$eq': str(team_shortName)}}]},
                                {'away_team_score': 1,
                                 'home_team_score': 1,
                                'home_team_shortName': 1,
                                'away_team_shortName': 1,
                                '_id': 0,
                                'gameweek': 1,
                                "id" : 1}
                                ).sort([('gameweek', -1)])
        return query

    def get_fixture_id(self, f_id):
        query = self.collection.find({'f_id': {'$eq': f_id}},
                                {'_id':0}
                                )
        return query


if __name__ == '__main__':
    test = DB('fixture_stats', 'EN_PR', '2019')
    query = test.get_five_latest_fixture_team('Arsenal')
    df = pd.DataFrame.from_dict(query)
    print(df)



