import os
import pymongo

from pprint import pprint

from pymongo import MongoClient

class DBConn():

    def __init__(self, DB_NAME='PremierLeague'):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[DB_NAME]

if __name__ == '__main__':
	db = DBConn()
	coll = db.DATABASE['team_standings']
	pipeline = [
		{
			'$match':{
				'seasonId': 363, 'team_id': 1
				}
		},
		{
			'$sort':{'$gameweek': -1}
		},
		{

			'$addFields':{'form': []}

		},
		{
			'$unwind': '$fixtures'
		},
		{
			'$project':{
				'form': {
					'$addToSet': {
						'$cond':{
							"if": {"$eq": ['team_id', 'fixtures.home_team_id']},
							"then": 5
						}
					}
				} 

			}
		}
	]
	test = coll.aggregate(pipeline)
	pprint(list(test))