from .load_files import deep_get
from .load_files import load_team_squads

def read_team_squads(data):
    """Read info from ...playerstats.json into flattened
    list of dicts. 
    """
    p_len = 0
    info_all = []
    for d in data:
        stats_temp = {}
        players = d['players']
        team = d['team']
        season = d['season']
        officials = d['officials']
        stats_temp = \
            {'seasonId': deep_get(season, 'id'),
             'seasonLabel': deep_get(season, 'label'),
             'teamName': deep_get(team, 'name'),
             'teamShortName': deep_get(team, 'club.shortName'),
             'teamAbbr': deep_get(team, 'club.abbr'),
             'teamId': deep_get(team, 'club.id'),
             'officials': [],
             'players': [],
            }
        for official in officials:
            officials_temp = \
            {'officialId': deep_get(official, 'officialId'),
             'role': deep_get(official, 'role'),
             'active': deep_get(official, 'active'),
             'birthLabel': deep_get(official, 'birth.date.label'),
             'birthMillis': deep_get(official, 'birth.date.millis'),
             'age': deep_get(official, 'age'),
             'name': deep_get(official, 'name.display'),
             'firstName': deep_get(official, 'name.first'),
             'lastName': deep_get(official, 'name.last'),
             'o_id': deep_get(official, 'id')
             }
            stats_temp['officials'].append(officials_temp)
        for player in players:
            players_temp = \
                {
                'playerId': deep_get(player, 'playerId'),
                'position': deep_get(player, 'info.position'),
                'shirtNum': deep_get(player, 'info.shirtNum'),
                'positionInfo': deep_get(player, 'info.positionInfo'),
                'nationalTeam': deep_get(player, 'nationalTeam.country'),
                'height': deep_get(player, 'height'),
                'weight': deep_get(player, 'weight'),
                'latestPostion': deep_get(player, 'latestPosition'),
                'appearances': deep_get(player, 'appearances', 0),
                'cleanSheets': deep_get(player, 'cleanSheets', 0),
                'saves': deep_get(player, 'saves', 0),
                'goalsConceded': deep_get(player, 'goalsConceded', 0),
                'awards': deep_get(player, 'awards'),
                'keyPasses': deep_get(player, 'keyPasses', 0),
                'tackles': deep_get(player, 'tackles', 0),
                'assists': deep_get(player, 'assists', 0),
                'goals': deep_get(player, 'goals', 0),
                'shots': deep_get(player, 'goals', 0),
                'joinDateLabel': deep_get(player, 'joinDate.label'),
                'joinDateMillis': deep_get(player, 'joinDate.millis'),
                'birthDateMillis': deep_get(player, 'birth.date.millis'),
                'birthDateLabel': deep_get(player, 'birth.date.label'),
                'country': deep_get(player, 'birth.country.country'),
                'countryDemonym': deep_get(player, 'birth.country.demonym'),
                'countryIsoCode': deep_get(player, 'birth.country.isoCode'),
                'birthPlace': deep_get(player, 'birth.place'),
                'age': deep_get(player, 'age'),
                'name': deep_get(player, 'name.display'),
                'firstName': deep_get(player, 'name.first'),
                'lastName': deep_get(player, 'name.last'),
                'p_id': deep_get(player, 'id')
                }
            stats_temp['players'].append(players_temp)
        info_all.append(stats_temp)
    return info_all

def team_squads(league, year):
    """Returns team squads"""
    squads = read_team_squads(load_team_squads(league, year))
    return squads
    

if __name__ == '__main__':
    team_squads('EN_PR', 2019)