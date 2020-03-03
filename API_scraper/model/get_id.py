from api_scraper import *
from directory import Directory
import re
from functools import lru_cache
import cProfile



class Params():

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

	def get_team_param():
		pass



if __name__ == '__main__':
	p = Params()
	p.league_season()


