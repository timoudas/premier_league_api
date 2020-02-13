import requests
import json
from pprint import pprint
import os.path


class PremierLeague:
	
	def __init__(self, base_url='https://footballapi.pulselive.com/football'):
		self.base_url = base_url
		self.dirname = os.path.dirname(__file__)
		self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
						'Origin': 'https://www.premierleague.com',
						'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
						}

	
	def save_json(self,file, filename):
		file = os.path.join(self.dirname, "../json/" + str(file) + ".json" )
		with open(file, "w") as f:
			#pretty prints and writes the same to the json file 
			f.write(json.dumps(filename, indent=4, sort_keys=False))
		
	def get_competion_id(self):

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
		
		self.save_json("competitions", competitions)

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
				print(club['name'])
				print(club['teams'][0]['id'])
				clubs[club['name']] = club['teams'][0]['id']

			page += 1
			if page == response["pageInfo"]["numPages"]:
				break
			
		self.save_json("clubs", clubs)

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

		self.save_json("fixtures_unplayed", fixtures_unplayed)
		self.save_json("fixtures_played", fixtures_played)
		self.save_json("fixtures", fixtures)

	def get_standings(self, compSeasons):

		url = self.base_url + '/compseasons/{}/standings'.format(compSeasons)
		
		
		params = (
			('pageSize', '100'),
				)
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


		self.save_json("standings", standings)

	def get_team_standing(self, compSeasons, teamId):

		url = self.base_url + '/compseasons/{}/standings/team/{}'.format(compSeasons,teamId)
		
		params = (
			('pageSize', '100'),
				)
		response = requests.get(url, params = params, headers=self.headers).json() # request to obtain the team info


		team_standing = response['entries'] #team standing through season
		season_id = response['compSeason']['label'] #season label
		team = response['team'] #team name
		team_name = str(response['team']['name'])
		
		team_standings = {} #Store all standings


		#loop to get all info for all standings
		for standing in team_standing:
			standing_id = standing['played']
			index = standing_id

			team_standings[index] = \
			{
			'season' : season_id,
			'season_id' : standing['fixtures'][0]['gameweek']['compSeason']['id'],
			'team_id' : team['club']['id'],
			'team' : team['name'],
			'position' : standing['position'],
			'points' : standing['points'],
			'played_games' : standing['played'],
			'game_week_id' : standing['fixtures'][0]['gameweek']['id'],
			'game_week': standing['fixtures'][0]['gameweek']['gameweek'],
			'competition' : standing['fixtures'][0]['gameweek']['compSeason']['competition']['description'],
			'game_id' : standing['fixtures'][0]['id'],
			'home_team' : standing['fixtures'][0]['teams'][0]['team']['name'],
			'home_team_id' : standing['fixtures'][0]['teams'][0]['team']['club']['id'],
			'home_team_score': standing['fixtures'][0]['teams'][0]['score'],
			'away_team' : standing['fixtures'][0]['teams'][1]['team']['name'],
			'away_team_id' : standing['fixtures'][0]['teams'][1]['team']['club']['id'],
			'away_team_score': standing['fixtures'][0]['teams'][1]['score'] 
			}


		f = open(team_name + "_standings_" + str(compSeasons) + ".json", "w")

		# pretty prints and writes the same to the json file 
		f.write(json.dumps(team_standings,indent=4, sort_keys=False))
		f.close()



		

		 


if __name__ == "__main__":
	prem = PremierLeague()

	prem.get_clubs()





	
	
			
	





