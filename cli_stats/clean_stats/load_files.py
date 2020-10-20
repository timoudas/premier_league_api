from directory import Directory
from functools import reduce
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
    """Load fixture_info json files into a container
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
    """Load player/fixture stats json files into a container
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