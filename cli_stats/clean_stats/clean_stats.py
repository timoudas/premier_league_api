#!/usr/bin/python
"""
Cleanstats json json files with stats. Since most files come in a nested
format CleanStats flattens the file into list of dict where the dicts
are flattend with the relevant info. 

"""
#!/usr/bin/python
"""
Updates .json files with new data from the api if the json exists

Looks if fixtureID exists in .json, if it doesn't exist it gets append
"""


import collections
import sys
import uuid 

from directory import Directory
from functools import reduce
from pprint import pprint
from storage_config import StorageConfig

dirs = Directory()


def deep_get(dictionary, keys, default=None):
    """Get values of nested keys from dict
        Args:
            dictionary(dict): Dict with nested keys
            keys(dict.keys()): "." separated chain of nested keys, ex "info.player.name"
    """
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def load_player_stats(league, year):
    """Load player_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'{league}_{year}_playerstats.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_team_squads(league, year):
    """Load team_squads json files into a container
        Args:
            year(int): year of team_squads.json
    """
    try: 
        file = f'{league}_{year}_teamsquads.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_fixture_stats(league, year):
    """Load fixture_stats json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'{league}_{year}_fixturestats.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_fixture_info(league, year):
    """Load team_squads json files into a container
        Args:
            year(int): year of team_squads.json
    """
    try: 
        file = f'{league}_{year}_fixtureinfo.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_fixture_player_stats(league, year):
    """Load player_fixture json files into a container
        Args:
            year(int): year of team_squads.json
    """
    try: 
        file = f'{league}_{year}_player_fixture.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_team_standings(league, year):
    """Load team_standings json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'{league}_{year}_teamstandings.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        stats_file.append({'season': year})
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")

def load_league_standings(league, year):
    """Load league standings json files into a container
        Args:
            year(int): year of player_stats json
    """
    try: 
        file = f'{league}_{year}_league_standings.json'
        stats_file = dirs.load_json(file, StorageConfig.STATS_DIR)
        return stats_file
    except FileNotFoundError as e:
        print(file, "not found")


def read_playerstats(data):
    """Read stats from ...playerstats.json into flattened
    list of dicts. 
    """
    try:
        stats_all = []
        for d in data:
            stats_temp = {}
            if 'stats' in d:
                stats = d['stats']
                for dicts in stats:
                    stats_temp['id'] = dicts.get('id')
                    if dicts.get('name') != None:
                        stats_temp[dicts.get('name')] = dicts.get('value')
                stats_all.append(stats_temp)
        return stats_all
    except TypeError as e:
        print("Check that data exists and is loaded correctly")

def read_player_fixture_all(data):
    """Read stats from ...playerstats.json into flattened
    list of dicts. 
    """
    try:
        stats_all = []
        for d in data:
            stats_temp = {}
            if 'stats' in d:
                stats = d['stats']
                for dicts in stats:
                    stats_temp['id'] = dicts.get('id')
                    if dicts.get('name') != None:
                        stats_temp[dicts.get('name')] = dicts.get('value')
            if 'info' in d:
                stats = d['info']
                stats_temp.update(
                    {'age' : stats.get('age'),
                    'id' : stats.get('id'),
                    'birth' : deep_get(stats, 'birth.date.label'),
                    'birth_exact' : deep_get(stats, 'birth.date.millis'),
                    'country' : deep_get(stats, 'birth.country.country'),
                    'isoCode' : deep_get(stats, 'birth.country.isoCode'),
                    'loan' : deep_get(stats, 'info.loan'),
                    'position' : deep_get(stats, 'info.position'),
                    'positionInfo' : deep_get(stats, 'info.positionInfo'),
                    'shirtNum' : deep_get(stats, 'info.shirtNum'),
                    'name' : deep_get(stats, 'name.display'),
                    'first' : deep_get(stats, 'name.first'),
                    'last' : deep_get(stats, 'name.last'),
                    'nationalTeam' : deep_get(stats, 'nationalTeam.country'),
                    'playerId' : stats.get('playerId'),
                    'p_id' : stats.get('id'),})
            try:
                stats_temp = {'season' : data[-1]['season']}
            except KeyError as e:
                pass
            stats_all.append(stats_temp)
        return stats_all
    except TypeError as e:
        print("Check that data exists and is loaded correctly")

def read_playerinfo(data):
    """Read info from ...playerstats.json into flattened
    list of dicts. 
    """
    info_all = []
    # try:
    for d in data:
        stats_temp = {}
        if 'info' in d:
            stats = d['info']
            stats_temp = \
                {'age' : stats.get('age'),
                'id' : stats.get('id'),
                'birth' : deep_get(stats, 'birth.date.label'),
                'birth_exact' : deep_get(stats, 'birth.date.millis'),
                'country' : deep_get(stats, 'birth.country.country'),
                'isoCode' : deep_get(stats, 'birth.country.isoCode'),
                'loan' : deep_get(stats, 'info.loan'),
                'position' : deep_get(stats, 'info.position'),
                'positionInfo' : deep_get(stats, 'info.positionInfo'),
                'shirtNum' : deep_get(stats, 'info.shirtNum'),
                'name' : deep_get(stats, 'name.display'),
                'first' : deep_get(stats, 'name.first'),
                'last' : deep_get(stats, 'name.last'),
                'nationalTeam' : deep_get(stats, 'nationalTeam.country'),
                'playerId' : stats.get('playerId'),
                'p_id' : stats.get('id'),}
            try:
            	stats_temp = {'season' : data[-1]['season']}
            except KeyError as e:
            	pass
            info_all.append(stats_temp)
    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
    return info_all

def read_player_team(data):
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
                }
            stats_temp['id'] = player['id']
            info_all.append(stats_temp)
    return info_all

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

def validate_id(data):
    players = read_playerinfo(load_player_stats(data))
    squads = read_team_squads(load_team_squads(data))
    p_sort = sorted(players, key=lambda k: k['id']) 
    s_sort = sorted(squads, key=lambda k: k['id']) 

    keyed_players = {a["id"]:a for a in p_sort} # easier access for IN - check
    keyed_squads = {a["id"]:a for a in s_sort}  # easier access for IN - check

    # iterate players and modify them if squad info given, else printout info
    for player in p_sort:
        if player["id"] in keyed_squads:
            player.update(keyed_squads[player["id"]])
        else:
            print("Player", player["id"], "is not in squad info")
  

    # get squads without players
    for squad_player in keyed_squads:
        if squad_player not in keyed_players:
            print("Player", squad_player, "in squad is not in player info")

def fixture_player_stats(league, year):
    players_info = read_player_fixture_all(load_fixture_player_stats(league, year))
    # player_stats = read_playerstats(load_fixture_player_stats(league, year))
    print(len(players_info))
    #Mergers the two list of dicts if `id-key` is the same
    # merge_info_stats = [{**x, **y} for y in players_info for x in player_stats if x['id'] == y['id']]
    # d = [dict(sorted(d.items())) for d in merge_info_stats]
    return players_info

def playerstats(league, year):
    players_info = read_playerinfo(load_player_stats(league, year))
    player_stats = read_playerstats(load_player_stats(league, year))


    #Mergers the two list of dicts if `id-key` is the same
    merge_info_stats = [{**x, **y} for y in players_info for x in player_stats if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in merge_info_stats]
    return d

def read_fixtureinfo(data):
    info_all = []
    try:
        for d in data:
            stats_temp = {}
            if 'info' in d:
                stats = d['info']
                home_team = stats['teams'][0]
                away_team = stats['teams'][1]
                stats_temp = \
                    {'gameweek_id' : deep_get(stats, 'gameweek.id'),
                    'season_label' : deep_get(stats, 'gameweek.compSeason.label'),
                    'id' : stats['id'],

                    'competition' : deep_get(stats, 'gameweek.compSeason.competition.description'),
                    'competition_abbr' : deep_get(stats, 'gameweek.compSeason.competition.abbreviation'),
                    'competition_id' : deep_get(stats, 'gameweek.compSeason.competition.id'),

                    'gameweek' : deep_get(stats, 'gameweek.gameweek'),
                    'kickoff' : deep_get(stats, 'kickoff.label'),
                    'kickoff_millis' : deep_get(stats, 'kickoff.millis'),

                    'home_team' : stats['teams'][0]['team']['name'],
                    'home_team_id' : stats['teams'][0]['team']['club']['id'],
                    'home_team_shortName' : stats['teams'][0]['team']['shortName'],
                    'home_team_score' : deep_get(home_team, 'score', default=0),

                    'away_team' : stats['teams'][1]['team']['name'],
                    'away_team_id' : stats['teams'][1]['team']['club']['id'],
                    'away_team_shortName' : stats['teams'][1]['team']['shortName'],
                    'away_team_score' : deep_get(away_team, 'score', default=0),

                    'ground' : deep_get(stats, 'ground.name'),
                    'grounds_id' : deep_get(stats, 'ground.id'),

                    'city' : deep_get(stats, 'ground.city'),
                    'fixtureType' : stats.get('fixtureType'),
                    'extraTime' : stats.get('extraTime'),
                    'shootout' : stats.get('shootout'),
                    'status': stats.get('status'),

                    'clock_label' : deep_get(stats, 'clock.label'),
                    'clock_secs' : deep_get(stats, 'clock.secs'),}
                info_all.append(stats_temp)
    except TypeError as e:
        print("Check that data exists and is loaded correctly")
    return info_all

def read_fixturestats(data):
    """In key "stats" followed by teamID followed by key "M"

    """
    try:
        stats_all = []
        for d in data:
            stats_temp = {}
            stats_home = {}
            stats_away = {}
            if not 'stats' in d:
                try:
                    stats_temp['id'] = d['info']['id']
                    stats_all.append(stats_temp)
                except KeyError as e:
                    pass
            else:
                stats = d['stats']
                info = d['info']

                home_id_key = str(info['teams'][0]['team']['club']['id'])
                away_id_key = str(info['teams'][1]['team']['club']['id'])


                if away_id_key in stats:
                    if home_id_key in stats:
                        away = stats[away_id_key]['M']
                        home = stats[home_id_key]['M']
                        stats_away = {'away_' + stats.get('name'): stats.get('value') for stats in away}
                        stats_home = {'home_' + stats.get('name'): stats.get('value') for stats in home}
                        stats_temp.update(stats_away)
                        stats_temp.update(stats_home)
                        stats_temp.update({'id' : info['id']})

    

                stats_all.append(stats_temp)
        return stats_all
    except TypeError as e:
        print(e, "Check that data exists and is loaded correctly")

def read_fixture_events(data):
    info_all = []
    for d in data:
        match_officals = d['matchOfficials']
        half_time =d['halfTimeScore']
        team_list = d['teamLists']
        events = d['events']
        stats_temp = \
            { 'home_halftime' : half_time['homeScore'],
              'away_halftime' : half_time['awayScore'],
              'matchOfficials': [],
              'lineUps': [],
              'substitutes': [],
              'events' : [],
              'id': d['id'],
              'f_id': d['id'],
              'formation':[],

        }
        for official in match_officals:
            match_officals_temp = {}
            match_officals_temp = \
            {'role': deep_get(official, 'role'),
             'matchOfficialId': official['matchOfficialId'],
             'first': deep_get(official, 'name.first'),
             'last': deep_get(official, 'name.last'),
             'name': deep_get(official, 'name.display'),
             'm_id': official['id']
            }
            stats_temp['matchOfficials'].append(match_officals_temp)

        for lineups in team_list:
            if lineups:
                team_id = lineups['teamId']
                linup = lineups['lineup']
                substitutes = lineups['substitutes']
                formation = lineups['formation']
                formation_temp = \
                {'teamId': team_id,
                'label': formation['label'],
                'players': formation['players']
                }
                stats_temp['formation'].append(formation_temp)
                for l in linup:
                    lineup_temp = {}
                    lineup_temp = \
                    {'teamId': team_id,
                     'matchPosition': deep_get(l, 'matchPosition'),
                     'captain': deep_get(l, 'captain'),
                     'playerId': deep_get(l, 'playerId'),
                     'position': deep_get(l, 'info.position'),
                     'shirtNum': deep_get(l, 'info.shirtNum'),
                     'positionInfo': deep_get(l, 'info.positionInfo'),
                     'name': deep_get(l, 'name.display'),
                     'first': deep_get(l, 'name.first'),
                     'last': deep_get(l, 'name.last'),
                     'id': l['id'],
                    }
                    stats_temp['lineUps'].append(lineup_temp)

                for s in substitutes:
                    substitutes_temp = {}
                    substitutes_temp = \
                    {'teamId': team_id,
                     'matchPosition': deep_get(s, 'matchPosition'),
                     'captain': deep_get(s, 'captain'),
                     'playerId': deep_get(s, 'playerId'),
                     'position': deep_get(s, 'info.position'),
                     'shirtNum': deep_get(s, 'info.shirtNum'),
                     'positionInfo': deep_get(s, 'info.positionInfo'),
                     'name': deep_get(s, 'name.display'),
                     'first': deep_get(s, 'name.first'),
                     'last': deep_get(s, 'name.last'),
                     'id': s['id']
                    }
                
                    stats_temp['substitutes'].append(substitutes_temp)

        for event in events:
            if event:
                events_temp = {}
                events_temp = \
                {'clockSecs': deep_get(event, 'clock.secs'),
                 'clockLabel': deep_get(event, 'clock.label'),
                 'phase': deep_get(event, 'phase'),
                 'type': deep_get(event, 'type'),
                 'timeMillis': deep_get(event, 'time.millis'),
                 'timeLabel': deep_get(event, 'time.label'),
                 'homeScore': deep_get(event, 'score.homeScore'),
                 'awayScore': deep_get(event, 'score.awayScore'),
                 'id': deep_get(event, 'id'),
                }
            stats_temp['events'].append(events_temp)


        info_all.append(stats_temp)
    return info_all

def fixturestats(league, year):
    info = read_fixtureinfo(load_fixture_stats(league, year))
    stats = read_fixturestats(load_fixture_stats(league, year))
    events = read_fixture_events(load_fixture_info(league, year))


    #Mergers the two list of dicts if `id-key` is the same
    fixture_merged = [{**x, **y} for y in info for x in stats if x['id'] == y['id']]
    merge_events = [{**x, **y} for y in fixture_merged for x in events if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in merge_events]
    return d

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
                             'season_label': deep_get(d, 'season.label'),
                             'season_id': deep_get(d, 'season.id'),
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

def read_leagueinfo(data):
    info_all = []
    try:
        for d in data:
            league_stand_id = str(uuid.uuid4())[:8]
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


if __name__ == '__main__':
    # pprint(read_fixture_events(load_fixture_info('EN_PR', 2019)))
    pprint(read_playerstats(load_player_stats('EN_PR', '2019')))



