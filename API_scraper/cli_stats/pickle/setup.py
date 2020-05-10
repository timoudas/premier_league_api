import os
import pickle
import requests
import sys

sys.path.insert(0, 'api_scraper')
sys.path.insert(0, 'get_id')
sys.path.insert(0, 'get_stats')
sys.path.insert(0, '../directory')
from api_scraper import Football
from check_api import ValidateParams
from directory import Directory
from get_id import Params
from get_stats import SeasonStats
from get_stats import Stats
from pprint import pprint




# params = Params()
# validation = ValidateParams()
# stats = Stats().stats
# fb = Football()
with open('test_pickle', 'rb') as f:
    test = pickle.load(f)
    # test['EN_PR_2017/2018'].fixture_stats()
    # test['EN_PR_2018/2019'].fixture_stats()
    #test['EN_PR_2019/2020'].fixture_stats()
    # test['EN_PR_2017/2018'].team_standings()
    # test['EN_PR_2018/2019'].team_standings()
    test['EN_PR_2019/2020'].team_squad()
