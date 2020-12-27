from .get_stats_methods.get_leaguestandings import LeagueStats
from .get_stats_methods.get_teamstats import TeamStats
from .get_stats_methods.get_playerstats import PlayerStats
from .get_stats_methods.get_fixturestats import FixtureStats



class SeasonStats(PlayerStats, TeamStats, FixtureStats, LeagueStats):

    def __init__(self, *args, **kwargs):
        """Empty construtor for lazy initiation of inherited
        sub-classes."""
        pass

    def __call__(self, called_method, *args, **kwargs):
        """Calls a method from a sub-class

            Args:
                called_method (str): Existing method in one of the sub-classes
                *args (str): League and Season
        """
        if hasattr(PlayerStats, called_method):
            PlayerStats.__init__(self, *args, **kwargs)
            self.player_dispatch_map.get(called_method)()

        elif hasattr(TeamStats, called_method):
            TeamStats.__init__(self, *args, **kwargs)
            self.team_dispatch_map.get(called_method)()

        elif hasattr(FixtureStats, called_method):
            FixtureStats.__init__(self, *args, **kwargs)
            self.fixture_dispatch_map.get(called_method)()

        elif hasattr(LeagueStats, called_method):
            LeagueStats.__init__(self, *args, **kwargs)
            self.league_dispatch_map.get(called_method)()
        else:
            raise ValueError(f'The called "{called_method}" method was not found')


if __name__ == '__main__': 
    players = PlayerStats('EN_PR', '2019').load_season_players()
