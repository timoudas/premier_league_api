from directory import Directory
from directory import Storageconfig 
import pandas as pd
from pprint import pprint
from functools import reduce 

def load_team_standings(year):
    """Load player_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'EN_PR_{year}_teamstandings.json'
        stats_file = dirs.load_json(file, Storageconfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")