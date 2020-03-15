from api_scraper import Football
from get_id import Params
from get_stats import Stats
from get_stats import SeasonStats
from directory import Directory
from check_api import ValidateParams
import os
import pickle


# params = Params()
# validation = ValidateParams()
# stats = Stats().stats

with open('test_pickle', 'rb') as f:
    test = pickle.load(f)
    print(test['EN_PR_2019/2020'].season)
