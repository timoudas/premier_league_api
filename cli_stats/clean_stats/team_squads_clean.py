from load_files import deep_get
from load_files import load_team_squads

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
            }
        for official in officials:
            stats_temp = \
            {'officialId': deep_get(official, 'officialId'),
             'role': deep_get(official, 'role'),
             'active': deep_get(official, 'active'),
             'birthLabel': deep_get(official, 'birth.date.label'),
             'birthMillis': deep_get(official, 'birth.date.millis'),
             'age': deep_get(official, 'age'),
             'name': deep_get(official, 'name.display'),
             'firstName': deep_get(official, 'name.first'),
             'lastName': deep_get(official, 'name.last'),
             'o_id': deep_get(official, 'id')}
        for player in players:
            stats_temp = \
                {
                'playerId': deep_get(player, 'playerId'),
                'position': deep_get(player, 'info.position'),
                'shirtNum': deep_get(player, 'info.shirtNum'),
                'positionInfo': deep_get(player, 'info.positionInfo'),
                'nationalTeam': deep_get(player, 'nationalTeam.contry'),
                'height': deep_get(player, 'height'),
                'weight': deep_get(player, 'weight'),
                'latestPostion': deep_get(player, 'latestPostion'),
                'appearances': deep_get(player, 'appearances', 0),
                'cleanSheets': deep_get(player, 'cleanSheets', 0),
                'saves': deep_get(player, 'saves', 0),
                'goalsConceded': deep_get(player, 'goalsConceded', 0),
                'awards': deep_get(player, 'awards'),
                'keyPasses': deep_get(player, 'keyPasses', 0),
                'tackles': deep_get(player, 'tackles', 0),
                'assists': deep_get(player, 'assists', 0),
                'joinDateLabel': deep_get(player, 'joinDate.label'),
                'joinDateMillis': deep_get(player, 'joinDate.millis'),
                'leaveDateLabel': deep_get(player, 'leaveDate.label'),
                'leaveDateMillis': deep_get(player, 'leaveDate.millis'),


                }
            stats_temp['id'] = player['id']
            info_all.append(stats_temp)
    return info_all

def team_squads(league, year):
    squads = read_team_squads(load_team_squads(league, year))
    print(len(squads))

if __name__ == '__main__':
    team_squads('EN_PR', 2019)