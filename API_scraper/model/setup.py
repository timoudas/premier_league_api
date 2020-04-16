from api_scraper import Football
from get_id import Params
from get_stats import Stats
from get_stats import SeasonStats
from directory import Directory
from check_api import ValidateParams
import os
import pickle
import requests
from pprint import pprint




# params = Params()
# validation = ValidateParams()
# stats = Stats().stats
# fb = Football()
with open('league_seasons_init', 'rb') as f:
    test = pickle.load(f)
    test['EN_PR_2017/2018'].player_stats()
    test['EN_PR_2018/2019'].player_stats()
    test['EN_PR_2019/2020'].player_stats()
