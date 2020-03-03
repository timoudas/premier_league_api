from api_scraper import *
from directory import Directory
import re
from functools import lru_cache
import cProfile
from tqdm import tqdm
import time


class Params():
	_temp_season = {}

	def __init__(self):
		self.fb = Football()
		self.fb_league = self.fb.load_leagues()
		self.dir = Directory()

	def season_label(self, label):
		try:
			return re.search( r'(\d{4}/\d{4})', label).group()	
		except: 
			label = re.search( r'(\d{4}/\d{2})', label).group()
			return re.sub(r'(\d{4}/)', r'\g<1>20', label)
			

	def league(self):
		league_info = {}
		for league in self.fb_league.values():
			league_info.update({league['abbreviation']: league['id']})
			#league_info.append(info)
		self.dir.mkdir('..', 'json', 'params')
		self.dir.save_json('league_params', league_info, '..', 'json', 'params')


	def league_season(self):
		league_abbreviation = [league['abbreviation'] for league in self.fb_league.values()]
		season_info = {}
		for abbreviation in league_abbreviation:
			league_info = self.fb_league[abbreviation].load_seasons()
			season_info[abbreviation] = []
			for i in league_info.values():
				season_info[abbreviation] += [self.season_label(i['label'])]
		self.dir.save_json('season_params', season_info, '..', 'json', 'params')


		# self.dir.mkdir('..', 'json', 'params')
		# self.dir.save_json('league_params', league_info, '..', 'json', 'params')

	def get_team_param(self):
		"""Example of what we want to do"""

		teams = {}
		league_season = self.dir.load_json('season_params.json', '..', 'json', 'params')
		for league, season in tqdm(league_season.items()):
			self.fb.leagues[str(league)].load_seasons()
			for season_label in season:
				league_team = self.fb.leagues[str(league)].seasons[str(season_label)].load_teams()
				for team, val in league_team.items():
					if team not in teams:
						teams.update({team:val})
						teams[team].update({'championships':{league:[]}})
					elif league in teams[team]['championships'] and league in val:
						teams[team]['championships'][league].append(str(season_label))	
					elif league in
						teams[team]['championships'].update({league: []})
						
			pprint(teams)
		self.dir.save_json('test_teams_params', teams, '..', 'json', 'params')



if __name__ == '__main__':
	

	p = Params()
	p.get_team_param()

	# def get_team_param(self):
	# 	"""Example of what we want to do

	# 	Initializes the team dict, and loads json with league and season abbreviation


 #            "1": {
 #                "name": "Arsenal",
 #                "club": {
 #                    "name": "Arsenal",
 #                    "shortName": "Arsenal",
 #                    "abbr": "ARS",
 #                    "id": 1.0
 #                },
 #                "teamType": "FIRST",
 #                "grounds": [
 #                    {
 #                        "name": "Emirates Stadium",
 #                        "city": "London",
 #                        "capacity": 60272.0,
 #                        "location": {
 #                            "latitude": 51.5548,
 #                            "longitude": -0.108533
 #                        },
 #                        "source": "OPTA",
 #                        "id": 52.0
 #                    }
 #                ],
 #                "shortName": "Arsenal",
 #                "id": 1,
 #                "competition": 1
 #                "championships":{"EN_PR": {"seasons" : {"2019/2020": 2019/2020,
 #                								  "2018/2020": 2018/2020},
 #                			"CL_UC": "seasons" : {"2019/2020": 2019/2020,
 #                								  "2018/2020": 2018/2020},
 #                }

	# 	"""


	# 	#pprint(fb.leagues['EU_CL'].seasons['2019/2020'].load_teams())
	# 	teams = {}
	# 	league_season = self.dir.load_json('season_params.json', '..', 'json', 'params')
	# 	for league, season in tqdm(league_season.items()):
	# 		teams[league] = {}
	# 		for season_label in season:
	# 			teams[league].update({season_label:{}})
	# 			self.fb.leagues[str(league)].load_seasons()
	# 			teams[league][season_label].update(self.fb.leagues[str(league)].seasons[str(season_label)].load_teams())
	# 	self.dir.save_json('all_teams_params', teams, '..', 'json', 'params')


