from .load_files import deep_get
from .load_files import load_team_standings

def read_team_standings_stats(data):
    info_all = []
    try:
        for d in data:
                stats_temp = {}
                comp = d['season']
                standing = d['standing']
                team = d['team']
                for fixtures in standing:
                    if fixtures:
                        player_fixtures = fixtures['fixtures']

                        stats_temp = \
                            {'team' : deep_get(team, 'name'),
                            'team_id' : deep_get(team, 'club.id'),
                            'team_shortName' : deep_get(team, 'club.shortName'),
                             'competition' : deep_get(comp, 'competition.description'),
                             'competition_abbr' : deep_get(comp, 'competition.abbreviation'),
                             'competition_id' : deep_get(comp, 'competition.id'),
                             'seasonLabel': deep_get(d, 'season.label'),
                             'seasonId': deep_get(d, 'season.id'),
                             'fixtures' : [],
                             'played' : fixtures['played'],
                             'points' : fixtures['points'],
                             'position' : fixtures['position']}

        
                    for fixture in player_fixtures:
                        fixture_temp = {}
                        fixture_temp = \
                        {'home_team' : fixture['teams'][0]['team']['name'],
                         'home_team_id' : fixture['teams'][0]['team']['club']['id'],
                         'home_team_shortName' : fixture['teams'][0]['team']['shortName'],
                         'home_team_score' : fixture['teams'][0]['score'],

                         'away_team' : fixture['teams'][1]['team']['name'],
                         'away_team_id' : fixture['teams'][1]['team']['club']['id'],
                         'away_team_shortName' : fixture['teams'][1]['team']['shortName'],
                         'away_team_score' : fixture['teams'][1]['score'],
                         'ground' : fixture['ground']['name'],
                         'grounds_id' : fixture['ground']['id'],

                         'city' : fixture['ground']['city'],
                         'fixtureType' : fixture['fixtureType'],
                         'extraTime' : fixture['extraTime'],
                         'shootout' : fixture['shootout'],
                         'f_id' : fixture['id'],

                         'clock_label' : fixture['clock']['label'],
                         'clock_secs' : fixture['clock']['secs'],
                         'gameweekId': fixture['gameweek']['id'],
                         'gameweek': fixture['gameweek']['gameweek'],
                         'kickoffLabel': fixture['kickoff']['label'],
                         'kickoffMillis': fixture['kickoff']['millis']
                        }
                        stats_temp.update({
                            'gameweek': fixture['gameweek']['gameweek'],
                            'gameweekId': fixture['gameweek']['id'],
                            })


                        stats_temp['fixtures'].append(fixture_temp)           
                    info_all.append(stats_temp)
    except KeyError as e:
        pass
    return info_all

def team_standings(league, year):
    """Returns team standings"""
    stats = read_team_standings_stats(load_team_standings(league, year))
    return stats