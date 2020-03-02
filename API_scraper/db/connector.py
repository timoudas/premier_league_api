import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://admin:kommer10@db-k0ycg.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['db']
collection = db['player']

post = {'_id': 0, 'name': 'tim', 'score': 5}

collection.insert_one(post)