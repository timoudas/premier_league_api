from .load_files import deep_get
from .load_files import load_league_standings

def read_leagueinfo(data):
    info_all = []
    try:
        for d in data:
            stats_temp = {}
            overall = d['overall']
            home = d['home']
            away = d['away']
            grounds = d['ground']
            team = d['team']

            stats_temp = \
                {'team_name' : deep_get(team, 'name'),
                'team_shortName' : deep_get(team, 'club.shortName'),
                'team_id' : deep_get(team, 'club.id'), 
                'seasonId' : d['seasonId'],
                'seasondb Label' : d['seasonLabel'],
                'position' : d['position'],

                'overall': overall,
                'home': home,
                'away': away,

                'grounds_name' : deep_get(grounds, 'name'),
                'grounds_id' : deep_get(grounds, 'id'),
                'grounds_lat': deep_get(grounds, 'location.latitude'),
                'grounds_long': deep_get(grounds, 'location.longitude'),
                'grounds_city': deep_get(grounds, 'city'),}
            info_all.append(stats_temp)
    except TypeError as e:
        print("Check that data exists and is loaded correctly")
    return info_all

def league_standings(league, year):
    """Returns team standings"""
    stats = read_leagueinfo(load_league_standings(league, year))
    return stats