from load_files import deep_get
from load_files import load_player_stats

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
                'seasonId' : stats.get('seasonId'),
                'seasonLabelcle' : stats.get('seasonLabel'),
                'birth' : deep_get(stats, 'birth.date.label'),
                'birthExact' : deep_get(stats, 'birth.date.millis'),
                'country' : deep_get(stats, 'birth.country.country'),
                'isoCode' : deep_get(stats, 'birth.country.isoCode'),
                'loan' : deep_get(stats, 'info.loan'),
                'position' : deep_get(stats, 'info.position'),
                'positionInfo' : deep_get(stats, 'info.positionInfo'),
                'name' : deep_get(stats, 'name.display'),
                'first' : deep_get(stats, 'name.first'),
                'last' : deep_get(stats, 'name.last'),
                'nationalTeam' : deep_get(stats, 'nationalTeam.country'),
                'playerId' : stats.get('playerId'),
                'p_id' : stats.get('id'),}
            info_all.append(stats_temp)
    # except TypeError as e:
    #     print("Check that data exists and is loaded correctly")
    return info_all

def playerstats(league, year):
    players_info = read_playerinfo(load_player_stats(league, year))
    player_stats = read_playerstats(load_player_stats(league, year))

    #Mergers the two list of dicts if `id-key` is the same
    merge_info_stats = [{**x, **y} for y in players_info for x in player_stats if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in merge_info_stats]
    return 