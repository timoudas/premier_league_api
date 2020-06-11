import os

import pandas as pd

from pprint import pprint

from pymongo import MongoClient

class DB():

    def __init__(self, league, season):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.league = league
        self.season = season
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@database-mbqxj.mongodb.net/test?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client["Database"]
        self.collection = self.DATABASE[self.league + self.season]

    
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
            { "l_id": { "$exists": "true" }},
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
                                {'t_id': {'$exists':'true'},
                                'team_shortName': {'$eq': str(team_shortName)}},
                                {'home_team_shortName': 1,
                                'away_team_shortName': 1,
                                'home_team_score': 1,
                                'away_team_score': 1,
                                '_id': 0,
                                'gameweek': 1,
                                'fixture_id' : 1}
                                ).sort([('gameweek', -1)]).limit(limit)
        return query

    def get_fixture_id(self, f_id):
        query = self.collection.find({'f_id': {'$eq': f_id}},
                                {'_id':0}
                                )
        return query


if __name__ == '__main__':
    test = DB('EN_PR', '2019')
    query = test.get_fixture_id(46855)
    df = pd.DataFrame.from_dict(query)
    print(df)



