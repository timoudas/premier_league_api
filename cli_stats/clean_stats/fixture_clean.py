from .load_files import deep_get
from .load_files import load_fixture_info
from .load_files import load_fixture_player_stats
from .load_files import load_fixture_stats
from pprint import pprint



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
                    'seasonLabel' : deep_get(stats, 'gameweek.compSeason.label'),
                    'seasonId' : deep_get(stats, 'gameweek.compSeason.id'),
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
                formation = deep_get(lineups, 'formation')
                formation_temp = \
                {'teamId': team_id,
                'label': deep_get(formation, 'label'),
                'players': deep_get(formation, 'players')
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
                    'f_id': stats.get('f_id'),
                    'id' : stats.get('id'),
                    'seasonId' : stats.get('seasonId'),
                    'seasonLabel' : stats.get('seasonLabel'),
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
            stats_all.append(stats_temp)
        return stats_all
    except TypeError as e:
        print("Check that data exists and is loaded correctly")

def fixturestats(league, year):
    info = read_fixtureinfo(load_fixture_stats(league, year))
    stats = read_fixturestats(load_fixture_stats(league, year))
    events = read_fixture_events(load_fixture_info(league, year))


    #Mergers the two list of dicts if `id-key` is the same
    fixture_merged = [{**x, **y} for y in info for x in stats if x['id'] == y['id']]
    merge_events = [{**x, **y} for y in fixture_merged for x in events if x['id'] == y['id']]
    d = [dict(sorted(d.items())) for d in merge_events]
    return d

def fixture_player_stats(league, year):
    players_info = read_player_fixture_all(load_fixture_player_stats(league, year))
    return players_info