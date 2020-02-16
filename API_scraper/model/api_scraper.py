import os.path
import json
import requests



class ApiScraper:

    def __init__(self, base_url='https://footballapi.pulselive.com/football'):
        """
        Initializes the base_url for the API and the working directory
        """
        self.base_url = base_url
        self.dirname = os.path.dirname(__file__) #Set working directory
        #Required header to not get 403-Error from API
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                        }

    def save_json(self, file, filename, folder):
        """save dictionarirys to .json files        
        Args:
            file (str): The name of the file that is to be saved in .json format
            filename (dict): The dictionary that is to be wrote to the .json file
            folder (str): The folder name in the target directory
        """
        file = os.path.join(self.dirname, "../json/" + folder + "/" + str(file) + ".json" ) 
        with open(file, "w") as f:
            #pretty prints and writes the same to the json file
            f.write(json.dumps(filename, indent=4, sort_keys=False))

    def load_json(self, folder, file_name):
        """load json files
        Args:
            folder(str): The folder name that the requested file exist in
            file_name(str): The file name of the requested file
        """
        return os.path.join(self.dirname, '..', 'json', folder, file_name + '.json')

    def get_competion_id(self):
        """get Ids for competitions on API, returns a .json file saved in 
        ../json/competitions/competitions.json    
        json file contains IDs for each competition in the API.
        """
        url = self.base_url + '/competitions' #Set url for competitions
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        # request to obtain the id values and corresponding competition
        response = requests.get(url, params=params, headers=self.headers).json()
        all_comps = response["content"]
        competitions = {} #Dict that holds all data from API

        for comp in all_comps: #Iterate over all items in the API
            competition_id = comp['description'] #Get dict parent-keys
            index = competition_id #Set parent-keys as index for the the dict
            competitions[index] = \
                 {
                 'abbreviation': comp["abbreviation"],
                  'id' : comp['id'],
                 }
            
        #Save dict to json
        self.save_json("competitions", competitions, folder="competitions")

    def get_compseason(self, comp_id, competition_name, competition_abbr):
        """get Ids for all seasons for a competition on API, returns a .json file saved in
        ../json/competitions/comp_seasons_id_abbreviation.json
        json file contains IDs for a competition in the API.

        Args:
            id (str): The competions id
            competition_name (str): The name of the competion
            competions_abbr (str): The abbreviation of the competions
        """
        compseasons = {} #Dict to store att season IDs

        url = self.base_url + '/competitions/{}/compseasons'.format(comp_id)
        print(url)
        params = (('pageSize', '100'),)#adds ?pageSize=100 to url
        response = requests.get(url, params = params, headers=self.headers).json()
        competions_info = response['content']
        for comp_seasons in competions_info:
            index = competition_name #Set's gameIDs as index for dictionairy
            compseasons[index] = {comp_seasons['label']:{}}
            compseasons[index]['label'] = \
            {
            'label' : comp_seasons['label'],
            'id':comp_seasons['id']
            }

        self.save_json("comp_seasons_" + str(comp_id) + "_" + str(competition_abbr), compseasons, folder="seasons")

    def get_all_compseasons(self):
        """Gets compseasons for all the competition on API and creates a .json file with 
        compseasons for each competion seperatly """
        path = self.load_json('competitions','competitions') #Set path for competions.json
        with open(path, 'r') as comps:
            competitions = json.load(comps)
            #Holds all competition IDs
            competitions_id = [str(int(comp['id'])) for comp in competitions.values()]
            #Holds all competition names
            competitions_name = [str(comp) for comp in competitions.keys()]
            #Holds all competion abbreviations
            competitions_abbre = [str(comp['abbreviation']) for comp in competitions.values()]

            for comp_id, comp_name, comp_abbre in zip(competitions_id, competitions_name,competitions_abbre):
                self.get_compseason(comp_id, comp_name, comp_abbre)


    def get_clubs(self):
        """get Ids for all clubs on API, returns a .json file saved in ../json/clubs/clubs.json
        
        json file contains IDs for each club in the API.    
        """
        clubs = {} #Store all clubs
        url = self.base_url + '/clubs' #Set url 
        page = 0 #starting value of page
        while True:
            params = (
                ('pageSize', '100'),
                ('page', str(page))
                    )
            
            # request to obtain the club info
            response = requests.get(url, params = params, headers=self.headers).json()          
            all_clubs = response["content"]
            #loop to get all info for all competitions
            for club in all_clubs: 
                clubs[club['name']] = club['teams'][0]['id']

            page += 1
            if page == response["pageInfo"]["numPages"]:
                break

        self.save_json("clubs", clubs, folder="clubs")

    def get_fixtures(self,compSeasons):
        """get Ids and other info for all fixture on API, returns a .json file saved in ../json/clubs/clubs.json
        
        json file contains IDs for each club in the API.    
        """
        url = self.base_url + '/fixtures' 
        fixtures_unplayed = {} #Store info for not played fixtures
        fixtures_played = {} #Store all clubs

        page = 0 #starting value of page
        while True:
            params = (
                ('pageSize', '100'), #adds ?pageSize=100 to url
                ('page', str(page)),
                ('compSeasons', str(compSeasons)),
                    )
            
            # request to obtain the team info
            response = requests.get(url, params = params, headers=self.headers).json()
            all_games = response["content"]
            #loop to get info for each game 

            for game in all_games: #Iterates over all games

                if game['status'] == 'U': #Checks if game is un-played
                    game_id = game['id'] #Get's the gameIDs for each game
                    index = game_id #Set's gameIDs as index for dictionairy
                    fixtures_unplayed[index] = \
                        {
                        'match' : game_id,
                        'kickoff' : game['fixtureType'],
                        'preli_date' : game['provisionalKickoff']['label'],
                        'scientific_date' : game['provisionalKickoff']['millis'],
                        'home_team' : game['teams'][0]['team']['name'],
                        'home_team_id' : game['teams'][0]['team']['club']['id'],
                        'home_team_abbr' : game['teams'][0]['team']['club']['abbr'],
                        'away_team' : game['teams'][1]['team']['name'],
                        'away_team_id' : game['teams'][1]['team']['club']['id'],
                        'away_team_abbr' : game['teams'][1]['team']['club']['abbr'],
                        'grounds' : game['ground']['name'],
                        'grounds_id' : game['ground']['id'],
                        'gameweek' : game['gameweek']['gameweek'],
                        'status' : game['status'],
                        }


            for game in all_games: 

                if game['status'] == 'C': #Check's if game is played
                    game_id = game['id'] #Get's the gameIDs for each game
                    index = game_id #Set's gameIDs as index for dictionairy
                    fixtures_played[index] = \
                    {
                    'match' : game['id'],
                    'kickoff' : game['fixtureType'],
                    'preli_date' : game['provisionalKickoff']['label'],
                    'scientific_date' : game['provisionalKickoff']['millis'],
                    'home_team' : game['teams'][0]['team']['name'],
                    'home_team_id' : game['teams'][0]['team']['club']['id'],
                    'home_team_abbr' : game['teams'][0]['team']['club']['abbr'],
                    'home_team_score' : game['teams'][0]['score'],
                    'away_team' : game['teams'][1]['team']['name'],
                    'away_team_id' : game['teams'][1]['team']['club']['id'],
                    'away_team_abbr' : game['teams'][1]['team']['club']['abbr'],
                    'away_team_score' : game['teams'][1]['score'],
                    'grounds' : game['ground']['name'],
                    'grounds_id' : game['ground']['id'],
                    'gameweek' : game['gameweek']['gameweek'],
                    'outcome' : game['outcome'],
                    'extraTime'  : game['extraTime'],
                    'shootout' : game['shootout'],
                    'played_time' : game['clock']['secs'],
                    'played_time_label' : game['clock']['label'],
                    'status' : game['status'],
                    'goals' : game['goals'],
                    }

            page +=1
            if page == response["pageInfo"]["numPages"]:
                break

        fixtures = dict(fixtures_unplayed)
        fixtures.update(fixtures_played)

        self.save_json("fixtures_unplayed", fixtures_unplayed, folder="fixtures")
        self.save_json("fixtures_played", fixtures_played, folder="fixtures")
        self.save_json("fixtures", fixtures, folder="fixtures")

    def get_standings(self, compSeasons):
        """Returns the table"""

        url = self.base_url + '/compseasons/{}/standings'.format(compSeasons)
        params = (('pageSize', '100'),)
        response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info
        all_standings = response["tables"][0]['entries']
        season_id = response['compSeason']['id']        
        standings = {} #Store all standings


        #loop to get all info for all standings
        for standing in all_standings:
            standing_id = standing['team']['name']
            index = standing_id
            standings[index] = \
            {
            'season_id' : season_id,
            'team_id' : standing['team']['club']['id'],
            'position' : standing['position'],
            'overall' : standing['overall'],
            'home' : standing['home'],
            'away' : standing['away'],
            }


        self.save_json("standings", standings, folder="standings")

    def get_team_standing(self, compSeasons, teamId):
        """returns a teams standings"""

        url = self.base_url + '/compseasons/{}/standings/team/{}'.format(compSeasons,teamId)        
        params = (
            ('pageSize', '100'),
                )
        # request to obtain the team info
        response = requests.get(url, params = params, headers=self.headers).json()
        team_standing = response['entries'] #team standing through season
        season = response['compSeason']['label'] #season label
        season_id = response['compSeason']['id'] #season label
        team = response['team'] #team name
        team_name = str(response['team']['name'])       
        team_standings = {} #Store all standings

        #loop to get all info for all standings
        for standing in team_standing:
            if 'fixtures' in standing:
                standing_id = standing['played']
                index = standing_id

                team_standings[index] = \
                {
                'season' : season,
                'season_id' : season_id,
                'team_id' : team['club']['id'],
                'team' : team['name'],
                'position' : standing['position'],
                'points' : standing['points'],
                'played_games' : standing['played'],
                 'game_week_id' : standing['fixtures'][0]['id'],
                 'game_week': standing['fixtures'][0]['gameweek']['gameweek'],
                 'competition' : standing['fixtures'][0]['gameweek']['compSeason']['competition']['description'],
                 'game_id' : standing['fixtures'][0]['id'],
                 'home_team' : standing['fixtures'][0]['teams'][0]['team']['name'],
                 'home_team_id' : standing['fixtures'][0]['teams'][0]['team']['club']['id'],
                 'home_team_score': standing['fixtures'][0]['teams'][0]['score'],
                 'away_team' : standing['fixtures'][0]['teams'][1]['team']['name'],
                 'away_team_id' : standing['fixtures'][0]['teams'][1]['team']['club']['id'],
                 'away_team_score': standing['fixtures'][0]['teams'][1]['score'],
                 }

        self.save_json(team_name + "_standings_" + str(compSeasons), team_standings, folder="standings")

    def premierleague_team_standings(self, compSeasons):
        """Get standings for each team, for each week"""
        teams=[]
        path=self.load_json('standings', 'standings')
        with open(path, 'r') as f:
            clubs=json.load(f)
            for club in clubs.values():
                teams.append(club['team_id'])
        for team in teams:
            self.get_team_standing(compSeasons, team)

    def get_all_player(self):
        """Get all players from API"""

        url = self.base_url + '/players'
        players = {} #Store all standings
            
        page = 0 #starting value of page
        while True:
            params = (('pageSize', '100'),)
            response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info
            all_players = response["content"]

            #loop to get all info for all standings
            for player in all_players:
                try: 
                    if 'playerId' in player:
                        player_id = player['playerId']
                        index = player_id

                        players[index] = \
                        {'position' : player['info']['position'],
                        'positionInfo' : player['info']['positionInfo'],
                        'nationalTeam' : player['nationalTeam']['country'],
                        'birth' : player['birth']['date']['millis'],
                        'age' : player['age']
                        }

                    if 'shirtNum' in player:
                        players[index] = {'shirtNum' : player['info']['shirtNum']}

                    if 'currentTeam' in player:
                        players[index] = \
                        {
                        'currentTeam' : player['currentTeam']['name'],
                        'currentTeam_id' : player['currentTeam']['club']['id'],
                            }
                except Exception as e:
                    print(e)
            page +=1
            if page == response["pageInfo"]["numPages"]:
                break


        self.save_json("players", players, folder="players")

    def get_premierleague_players(self, compSeasons):
        """Get all premier_league players"""
        teams = []
        path = self.load_json('standings', 'standings')
        with open(path, 'r') as standings_clubs:
            clubs = json.load(standings_clubs)
            for club in clubs.values(): 
                teams.append(club['team_id'])
        url = self.base_url + compseasons

        

         


if __name__ == "__main__":
    PREM = ApiScraper()

    PREM.get_all_compseasons()






        


    
    
            
    





