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
from directory import Directory 
from directory import StorageConfig 
from pprint import pprint
from functools import reduce 
import collections


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
    """Load player_stats json files into a container
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


def load_team_standings(league, year):
    """Load player_stats json files into a container
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



def read_playerstats(data):
    """Read stats from ...playerstats.json into flattened
    list of dicts. 
    """
    try:
        stats_all = []
        stats_temp = {}
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
                'season' : data[-1]['season']}
            info_all.append(stats_temp)
    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
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
                'team_shortName' : deep_get(team, 'club.shortName'),}
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

def playerstats(league, year):
    players_info = read_playerinfo(load_player_stats(league, year))
    squads = read_team_squads(load_team_squads(league, year))
    player_stats = read_playerstats(load_player_stats(league, year))


    #Mergers the two list of dicts if `id-key` is the same
    merge_info_squad = [{**x, **y} for y in players_info for x in squads if x['id'] == y['id']]
    merge_info_stats = res = [{**x, **y} for x in merge_info_squad for y in player_stats if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in merge_info_stats]
    return d



def read_fixtureinfo(data):
    info_all = []
    try:
        for d in data:
            stats_temp = {}
            if 'info' in d:
                stats = d['info']
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
                    'home_team_score' : stats['teams'][0]['score'],

                    'away_team' : stats['teams'][1]['team']['name'],
                    'away_team_id' : stats['teams'][1]['team']['club']['id'],
                    'away_team_shortName' : stats['teams'][1]['team']['shortName'],
                    'away_team_score' : stats['teams'][1]['score'],

                    'ground' : deep_get(stats, 'ground.name'),
                    'grounds_id' : deep_get(stats, 'ground.id'),

                    'city' : deep_get(stats, 'ground.city'),
                    'fixtureType' : stats.get('fixtureType'),
                    'extraTime' : stats.get('extraTime'),
                    'shootout' : stats.get('shootout'),
                    'fixture_id' : stats.get('id'),

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
            if 'stats' in d:
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

def fixturestats(league, year):
    info = read_fixtureinfo(load_fixture_stats(league, year))
    stats = read_fixturestats(load_fixture_stats(league, year))


    #Mergers the two list of dicts if `id-key` is the same
    fixture_merged = [{**x, **y} for y in info for x in stats if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in fixture_merged]
    return d


def read_team_standings_stats(data):
    info_all = []
    # try:
    for d in data:
        stats_temp = {}
        if 'standing' in d:
            stats_all = d['standing']
            team = d['team']
            for stats in stats_all:
                if 'fixtures' in stats:
                    comp = stats['fixtures'][0]
                    stats_temp = \
                        {'played' : stats['played'],
                        'points' : stats['points'],
                        'position' : stats['position'],
                        'team' : deep_get(team, 'name'),
                        'team_id' : deep_get(team, 'club.id'),
                        'team_shortName' : deep_get(team, 'club.shortName'),

                        'competition' : deep_get(comp, 'gameweek.compSeason.competition.description'),
                        'competition_abbr' : deep_get(comp, 'gameweek.compSeason.competition.abbreviation'),
                        'competition_id' : deep_get(comp, 'gameweek.compSeason.competition.id'),
                        'season_label': deep_get(d, 'season.label'),
                        'season_id': deep_get(d, 'season.id'),

                        'gameweek' : deep_get(comp, 'gameweek.gameweek'),
                        'kickoff' : deep_get(comp, 'kickoff.label'),
                        'kickoff_millis' : deep_get(comp, 'kickoff.millis'),

                        'home_team' : comp['teams'][0]['team']['name'],
                        'home_team_id' : comp['teams'][0]['team']['club']['id'],
                        'home_team_shortName' : comp['teams'][0]['team']['shortName'],
                        'home_team_score' : comp['teams'][0]['score'],

                        'away_team' : comp['teams'][1]['team']['name'],
                        'away_team_id' : comp['teams'][1]['team']['club']['id'],
                        'away_team_shortName' : comp['teams'][1]['team']['shortName'],
                        'away_team_score' : comp['teams'][1]['score'],
                        'ground' : comp['ground']['name'],
                        'grounds_id' : comp['ground']['id'],

                        'city' : comp['ground']['city'],
                        'fixtureType' : comp['fixtureType'],
                        'extraTime' : comp['extraTime'],
                        'shootout' : comp['shootout'],
                        'fixture_id' : comp['id'],

                        'clock_label' : comp['clock']['label'],
                        'clock_secs' : comp['clock']['secs'],}
                    
                info_all.append(stats_temp)
    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
    return info_all

def team_standings(league, year):
    """Returns team standings"""
    stats = read_team_standings_stats(load_team_standings(league, year))
    return stats


if __name__ == '__main__':
    pass
    #dirs.save_json('test', playerstats('EN_PR', 2019), StorageConfig.DB_DIR)



