import requests
from pprint import pprint
import json
import re
import pymongo
from pymongo import MongoClient
import os

class DB():

    def __init__(self, DB_NAME='PremierLeague'):
        self.db_user = os.environ.get('DB_user')
        self.db_pass = os.environ.get('DB_pass')
        self.MONGODB_URL = f'mongodb+srv://{self.db_user}:{self.db_pass}@cluster0-mbqxj.mongodb.net/<dbname>?retryWrites=true&w=majority'
        self.client = MongoClient(self.MONGODB_URL)
        self.DATABASE = self.client[DB_NAME]

def clean_text(text):
	regex = r"""(['"{}])"""
	result = re.sub(regex, "", text)
	regex1 = r"([.])"
	cleaned = re.sub(regex1, "_", result)
	return cleaned

def get_translation():
	translations = {}
	url = 'https://translations.platform.pulselive.com/premierleague/en.js'
	response = requests.get(url)
	text = response.content
	decode = text.decode("utf-8")
	lines = decode.splitlines()[2]
	split = lines.split(',')
	clean = []
	for line in split:
		clean.append(clean_text(line))
	for i in clean:
		if i.startswith('label_stat'):
			k,v = i.split(':')
			translations[k] = v
		elif i.startswith('label_match'):
			k,v = i.split(':')
			translations[k] = v
		elif i.startswith('label_player'):
			k,v = i.split(':')
			translations[k] = v
	return translations
pprint(get_translation())

if __name__ == '__main__':
	db = DB()
	trans = get_translation()
	db.DATABASE['translations'].insert(trans)
	print('done')