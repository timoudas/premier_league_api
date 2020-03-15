"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""


from api_scraper import Football
from pprint import pprint
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import sys
from directory import Directory
import requests
import re
import json


dir = Directory()
data = dir.load_json('season_params.json', '..', 'json', 'params')

print(**data)

class ParseJson:

	def __init__(self, league, seasons):
		self.league = league
		self.seasons = seasons


# for league, seasons in data.items():
# 	d = ParseJson(league, seasons)
