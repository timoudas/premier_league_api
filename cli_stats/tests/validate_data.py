from get_data.get_stats import PlayerStats
from database.mongo_db import DBConn
from database.mongo_db import import_json

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

if __name__ == '__main__':
    validate_len_players_2019()

