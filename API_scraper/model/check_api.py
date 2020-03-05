"""Checks if all needed information exist on api for a league by season.

Input: A leagueID to check

Output: Console output with True/False values if information exist

**How the class checks if data exists**:

User provides a known leagueID, a request is made with the ID to see which seasons
exist. 
If no seasonIDs exist, it stops else takes all the seasonIDs and stores them.
For each seasonID it checks if fixtures exists, if it exists it stores them and
uses them to see if fixture stats exists. 
If fixture stats exist it requests att teams in 

"""


from directory import Directory
import requests
from tqdm import tqdm
import sys

dir = Directory()

def import_id(file_id):
    return dir.load_json(file_id ,'..', 'json', 'params')

def make_request(url):

    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
              }
    params = (('pageSize', '100'),)           
    response = requests.get(url, params = params, headers=headers)
    return response.status_code



def check_current_season():
    failed = {}
    league = import_id('league_params.json')
    print('Checking leagues..')
    for league_name, league_id in league.items():
        status = make_request(f'https://footballapi.pulselive.com/football/competitions/{league_id}/compseasons/current')
        if status != 200:
            failed.update({league_name:league_id})
    return failed


def remove_failed_leagues(failed_leagues):
    league = import_id('league_params.json')
    for failed in failed_leagues.keys():
        if failed in league:
            del league[failed]
    return league

failed_leagues = check_current_season()
ok_leagues = remove_failed_leagues(failed_leagues)


