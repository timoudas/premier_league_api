
import pandas as pd

from mongo_query import DB

class DataInit():

    def __init__(self, league='EN_PR', season='2019'):
        self.db = DB(league, season)

    @staticmethod
    def to_df(query):
        return pd.DataFrame.from_dict(query)

    def team_standing(self):
        """Returns all documents with a t_id key"""
        query = self.db.get_teams_standing()
        df = self.to_df(query)
        df = df.drop('_id', 1)
        return df

    def team_names(self):
        """Returns all the unique team names"""
        query = self.db.get_teams()
        df = self.to_df({'teams': query})
        return df

    def league_standings(self):
        """Returns the league standings"""
        query = self.db.get_league_standings_overall()
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
        query = self.db.get_five_latest_fixture_team(team_shortName, limit)
        df = self.to_df(query)
        df = df.rename(columns={'home_team_shortName': 'HT', 'away_team_shortName': 'AT', 
                                'home_team_score': 'HT_score', 'away_team_score': 'AT_score'})
        return df

if __name__ == '__main__':
    init = DataInit()
    print(init.fixture_form_decending('Arsenal'))