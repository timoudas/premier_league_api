
import pandas as pd

from db_connector import FixturesDB
from db_connector import LeagueDB
from db_connector import PlayersDB
from db_connector import TeamsDB


class DataInit():

    def __init__(self, league='EN_PR', season='2019'):
        self.league = league
        self.season = season

    @staticmethod
    def to_df(query):
        return pd.DataFrame.from_dict(query)

    def team_standing(self):
        """Returns all documents with a t_id key"""
        db = TeamsDB(self.league, self.season)
        query = db.get_teams_standing()
        df = self.to_df(query)
        df = df.drop('_id', 1)
        return df

    def team_names(self):
        """Returns all the unique team names"""
        db = LeagueDB(self.league, self.season)
        query = db.get_league_teams()
        df = self.to_df({'teams': query})
        return df

    def league_standings(self):
        """Returns the league standings"""
        db = LeagueDB(self.league, self.season)
        query = db.get_league_standings_overall()
        df = self.to_df(query)
        cols = df.columns.tolist()
        cols = cols[1:2] + cols[0:1] + cols[2:]
        df = df[cols]
        df = df.rename(columns={'team_shortName': 'Club', 'position': 'Position', 'overall_played': 'Played',
                                'overall_won': 'W','overall_draw': 'D', 'overall_lost': 'L', 
                                'overall_goalsFor': 'GF', 'overall_goalsAgainst':'GA',
                                'overall_goalsDifference': 'GD', 'overall_points': 'Points'})
        return df

    def fixture_form_decending(self, team_shortName: str, limit=5):
        """Return the latest five games for a team,
            
            Args:
                team_shortName: A teams shortname
                limit: The number of latest games
        """
        db = FixturesDB(self.league, self.season)
        query = db.get_five_latest_fixture_team(team_shortName, limit)
        df = self.to_df(query)
        cols = df.columns.tolist()
        cols = cols[0:3] + cols[4:5] + cols[3:4]+cols[5:]
        df = df[cols]
        df = df.rename(columns={'home_team_shortName': 'HTeam', 'away_team_shortName': 'ATeam', 
                                'home_team_score': 'H', 'away_team_score': 'A', 'gameweek': 'G'})
        return df

if __name__ == '__main__':
    init = DataInit()
    print(init.fixture_form_decending('Arsenal'))