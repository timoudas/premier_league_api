from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
import time
import sys
import requests
import re
from pprint import pprint



headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
params = (('pageSize', '100'),)

    # request to obtain the team info
url ='https://footballapi.pulselive.com/football/teams/48/compseasons/66/staff'


import requests
import datetime

from dateutil.parser import parse as parsedate
r = requests.head(url, headers=headers)
url_time = r.headers.get('if-none-match', '')
print(url_time)
#url_date = parsedate(url_time)
# file_time = datetime.datetime.fromtimestamp(os.path.getmtime(test_pickle))
# if url_date > file_time :
#     print('hi')