from load_files import deep_get
from load_files import load_team_squads

def read_team_squads(data):
    """Read info from ...playerstats.json into flattened
    list of dicts. 
    """
    info_all = []

    for d in data:
        stats_temp = {}
        players = d['players']
        team = d['team']
        for player in players:
            stats_temp = \
                {'team' : team['name'],
                'team_id' : deep_get(team, 'club.id'),
                'team_shortName' : deep_get(team, 'club.shortName'),
                'hight': deep_get(player, 'height'),
                'weight': deep_get(player, 'weight'),
                'appearances': deep_get(player, 'appearances', 0),
                'cleanSheets': deep_get(player, 'cleanSheets', 0),
                'saves': deep_get(player, 'saves', 0),
                'goalsConceded': deep_get(player, 'goalsConceded', 0),
                'keyPasses': deep_get(player, 'keyPasses', 0),
                'tackles': deep_get(player, 'tackles', 0),
                'assists': deep_get(player, 'assists', 0),

                }
            stats_temp['id'] = player['id']
            info_all.append(stats_temp)

    return info_all

def team_squads(league, year):
	pass