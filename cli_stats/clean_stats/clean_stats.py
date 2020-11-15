#!/usr/bin/python
"""
Imports all cleaningstages for all the different cleaning
processes.
"""
import collections
import sys

from pprint import pprint

from .fixture_clean import fixture_player_stats
from .fixture_clean import fixturestats
from .league_standings_clean import league_standings
from .player_clean import playerstats
from .team_squads_clean import team_squads
from .team_standings_clean import team_standings


def validate_id(league, year):
    players = read_playerinfo(load_player_stats(league, year))
    squads = read_team_squads(load_team_squads(league, year))
    p_sort = sorted(players, key=lambda k: k['id']) 
    s_sort = sorted(squads, key=lambda k: k['id'])
    print(len(p_sort))
    print(len(s_sort))

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


if __name__ == '__main__':
    # pprint(read_fixture_events(load_fixture_info('EN_PR', 2019)))
    pprint(fixture_player_stats('EN_PR', '2019'))



