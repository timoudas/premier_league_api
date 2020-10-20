from load_files import deep_get
from load_files import load_league_standings

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
                'seasonLabel' : d['seasonLabel'],

                'position' : d['position'],
                'overall_played' : deep_get(overall, 'played'),
                'overall_won' : deep_get(overall, 'won', 0),
                'overall_draw' : deep_get(overall, 'drawn', 0),
                'overall_lost' : deep_get(overall, 'lost', 0),
                'overall_goalsFor' : deep_get(overall, 'goalsFor'),
                'overall_goalsAgainst' : deep_get(overall, 'goalsAgainst'),
                'overall_goalsDifference' : deep_get(overall, 'goalsDifference'),
                'overall_points' : deep_get(overall, 'points'),

                'home_played' : deep_get(home, 'played'),
                'home_won' : deep_get(home, 'won', 0),
                'home_draw' : deep_get(home, 'draw', 0),
                'home_lost' : deep_get(home, 'lost', 0),
                'home_goalsFor' : deep_get(home, 'goalsFor'),
                'home_goalsAgainst' : deep_get(home, 'goalsAgainst'),
                'home_goalsDifference' : deep_get(home, 'goalsDifference'),
                'home_points' : deep_get(home, 'points'),

                'away_played' : deep_get(away, 'played'),
                'away_won' : deep_get(away, 'won', 0),
                'away_draw' : deep_get(away, 'draw', 0),
                'away_lost' : deep_get(away, 'lost', 0),
                'away_goalsFor' : deep_get(away, 'goalsFor'),
                'away_goalsAgainst' : deep_get(away, 'goalsAgainst'),
                'away_goalsDifference' : deep_get(away, 'goalsDifference'),
                'away_points' : deep_get(away, 'points'),

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