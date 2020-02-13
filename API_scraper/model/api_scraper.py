import requests
import json
from pprint import pprint
import os.path
from tqdm import tqdm



class ApiScraper:

	def __init__(self, base_url='https://footballapi.pulselive.com/football'):
		"""Base url, working directory and headers to make request work"""
		self.base_url = base_url
		self.dirname = os.path.dirname(__file__)
		self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
						'Origin': 'https://www.premierleague.com',
						'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
						}

	def save_json(self, file, filename, folder):
		"""save json files"""
		file = os.path.join(self.dirname, "../json/" + folder + "/" + str(file) + ".json" )
		with open(file, "w") as f:
			#pretty prints and writes the same to the json file 
			f.write(json.dumps(filename, indent=4, sort_keys=False))

	def load_json(self, folder, file_name):
		"""load json files"""
		return os.path.join(self.dirname, '..', 'json', folder, file_name + '.json')


	def get_competion_id(self):
		"""get Ids for competitions on API"""
		url = self.base_url + '/competitions' 

		params = (('pageSize', '100'),)#adds ?pageSize=100 to url

		response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the id values and corresponding competition

		all_comps = response["content"]

		competitions = {}

		for comp in all_comps:

			competition_id = comp['description']
			index = competition_id
			competitions[index] = \
				 {
				 'abbreviation': comp["abbreviation"],
				  'id' : comp['id'],
				 }

		self.save_json("competitions", competitions, folder="competitions")

	def get_compseason(self):
		"""get season IDs for each competition on API"""
		competitions_id = []
		compseasons = {}
		label = {}
		path = self.load_json('competitions','competitions')
		with open(path, 'r') as f:
			competitions = json.load(f)
			for comp in competitions.values():
				competitions_id.append(str(int(comp['id'])))

		try:
			for comp_id in competitions_id:
				url = self.base_url + '/competitions/{}/compseasons'.format(comp_id)

				params = (('pageSize', '100'),)#adds ?pageSize=100 to url

				response = requests.get(url, params = params, headers=self.headers).json()

				all_compseasons = response['content']

				for comp in all_compseasons:
					competition_id = comp_id
					index = competition_id
					compseasons[index] = {comp['label'], comp['id']}
		except Exception as e:
			print(e)

		self.save_json("comp_seasons", compseasons, folder="seasons")


	def get_clubs(self):

		clubs = {} #Store all clubs
		url = self.base_url + '/clubs' 

		page = 0 #starting value of page
		while True:
			params = (
				('pageSize', '100'),
				('page', str(page))#adds ?pageSize=100 to url
					)
			response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info

			all_clubs = response["content"]

			#loop to get all info for all competitions
			for club in all_clubs: 
				clubs[club['name']] = club['teams'][0]['id']

			page += 1
			if page == response["pageInfo"]["numPages"]:
				break

		self.save_json("clubs", clubs, folder="clubs")

	def get_fixtures(self,compSeasons):

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
			response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info

			all_games = response["content"]

			#loop to get info for each game 
			for game in all_games: 

				if game['status'] == 'U':

					game_id = game['id']
					index = game_id
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

				if game['status'] == 'C':

					game_id = game['id']
					index = game_id
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

		url = self.base_url + '/compseasons/{}/standings/team/{}'.format(compSeasons,teamId)
		
		params = (
			('pageSize', '100'),
				)
		response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info


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

		#f = open(team_name + "_standings_" + str(compSeasons) + ".json", "w")

		# pretty prints and writes the same to the json file 
		#f.write(json.dumps(team_standings,indent=4, sort_keys=False))
		#f.clos

	def premierleague_team_standings(self, compSeasons):
		teams=[]
		path=self.load_json('standings', 'standings')
		with open(path, 'r') as f:
			clubs=json.load(f)
			for club in clubs.values():
				teams.append(club['team_id'])
		for team in teams:
			self.get_team_standing(compSeasons, team)

	def get_all_player(self):

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

	def get_premierleague_players(sel, compSeasons):
		teams = []
		path = self.load_json('standings', 'standings')
		with open(path, 'r') as f:
			clubs = json.load(f)
			for club in clubs.values():	
				teams.append(club['team_id'])


		

		 


if __name__ == "__main__":
	prem = ApiScraper()

	prem.get_compseason()






	
	
			
	





