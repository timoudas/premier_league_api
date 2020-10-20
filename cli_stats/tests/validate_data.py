from clean_stats.clean_stats import load_player_stats
from clean_stats.clean_stats import load_team_squads
from clean_stats.clean_stats import playerstats
from clean_stats.clean_stats import read_playerinfo
from clean_stats.clean_stats import read_playerstats
from clean_stats.clean_stats import read_team_squads
from clean_stats.clean_stats import validate_id
from database.mongo_db import DBConn
from database.mongo_db import import_json
from get_data.get_stats import PlayerStats
from pprint import pprint

def validate_len_players_2019():
    players = (import_json('EN_PR_2019_playerstats.json'))
    t = DBConn().DATABASE['player_stats']
    var = list(t.find({'seasonId': 274}))
    if len(players) == len(var):
        print('True')
        print(f'json: {len(players)}, db: {len(var)}')
    else:
        print(f'json: {len(players)}, db: {len(var)}')
        print(len(set(players)))

def map_players_to_team(league, year):
    info = read_playerinfo(load_player_stats(league, year))
    squad = read_team_squads(load_team_squads(league, year))
    stats = read_playerstats(load_player_stats(league, year))
    inf_stat, total = playerstats(league, year) 
    print(f'info: {len(info)}, stats: {len(stats)}, squad: {len(squad)}')
    print(f'inf_stats: {len(inf_stat)}, total: {len(total)}')
    ids = []
    n = 0
    for i in total:
        if i['id'] not in ids:
            ids.append(i['id'])
        else:
            n += 1
            print(i['id'])
    print(n)


if __name__ == '__main__':
    validate_len_players_2019()
    map_players_to_team('EN_PR', 2019)

