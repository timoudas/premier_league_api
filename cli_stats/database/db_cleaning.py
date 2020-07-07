import json
import sys

from pprint import pprint

sys.path.append('../../dashboard')

from db_connector import FixturesDB
from db_connector import LeagueDB
from db_connector import PlayersDB
from db_connector import TeamsDB

class DBCleaning:

	def __init__(self, league, season):
		self.league = league
		self.season	= season

	def goalkeeper_collection(self):
		pipeline = [
			{
				'$match':{
					'position': 'G'
				}
			},
			# {
			# 	'$project': {
			# 		'total_aerial': {'$add': ['$aerial_lost', '$aerial_won']},
			# 		'total_attempts_conceded': {'$add': ['$attempts_conceded_ibox', '$attempts_conceded_obox']},
			# 		'total_goal_kicks': 'goal_kicks',
			# 		'total_keeper_throws': 'keeper_throws',
			# 		'total_goals_conceded': 'goals_conceded',
			# 	},
			# },
		    {
		        '$project': {
		        	'name': 1,
		        	'_id': 0,
		        	'avgAccBackZonePass': {
		        		'$multiply': [
		        			{'$divide': ['$accurate_back_zone_pass', '$total_back_zone_pass']}, '$appearances']},
		        	'avgAccChippedPass': {
		        		'$multiply': [{'$divide': ['$accurate_chipped_pass', '$total_chipped_pass']}, '$appearances']},
		        	'avgAccFwdZonePass': {'$multiply': 
		        		[{'$divide': ['$accurate_fwd_zone_pass', '$total_fwd_zone_pass']}, '$appearances']},
		        	'avgAccGoalKicks': {'$multiply': 
		        		[{'$divide': ['$accurate_goal_kicks', '$goal_kicks']}, '$appearances']},

		        	'avgAccSweeper': {'$multiply': 
		        		[{'$divide': ['$accurate_keeper_sweeper', '$total_keeper_sweeper']}, '$appearances']},
		        	'avgAccTrows': {'$multiply': 
		        		[{'$divide': ['$accurate_keeper_throws', '$keeper_throws']}, '$appearances']},
		        	'avgAccLaunches': {'$multiply': 
		        		[{'$divide': ['$accurate_launches', '$total_launches']}, '$appearances']},
		        	'AvgAccLongBalls': {'$multiply': 
		        		[{'$divide': ['$accurate_long_balls', '$total_long_balls']}, '$appearances']},
		        	'AvgAccPasses': {'$multiply': 
		        		[{'$divide': ['$accurate_pass', '$total_pass']}, '$appearances']},
		        	'TotalAerials': {'$add': ['$aerial_lost', '$aerial_won']},
		        	'AvgWonAerials': {'$multiply': 
		        		[{'$divide': ['$aerial_won', {'$add': ['$aerial_lost', '$aerial_won']}]}, '$appearances']},
		        	'AvgLostAerials':{'$multiply': 
		        		[{'$divide': ['$aerial_lost', {'$add': ['$aerial_lost', '$aerial_won']}]}, '$appearances']},

		        	'AvgAttemptsConcededInBox': {'$multiply': 
		        		[{'$divide': ['$attempts_conceded_ibox', {'$add': ['$attempts_conceded_ibox', '$attempts_conceded_obox']}]}, '$appearances']},
		        	'AvgAttemptsConcededOutBox': {'$multiply': 
		        		[{'$divide': ['$attempts_conceded_obox', {'$add': ['$attempts_conceded_ibox', '$attempts_conceded_obox']}]}, '$appearances']},
		        	'TotalAttemptsConceded': {'$add': ['$attempts_conceded_ibox', '$attempts_conceded_obox']},

		        	'BlockedPass': '$blocked_pass',
		        	'ChallengeLost': '$challenge_lost',
		        	'CleanSheets': '$cleanSheets',
		        	'OddsCleanSheets': {
		        		'$divide': [
		        			{'$divide': [
		        				'$cleanSheets', {'$subtract': ['$appearances', '$cleanSheets']}
		        			]}, 
							{'$add': 
								[1, {'$divide': ['$cleanSheets', {'$subtract': ['$appearances', '$cleanSheets']}]}]}]
		        	},
		        	'CrossesNotClaimed': '$cross_not_claimed',
		        	'DiveCatches': '$dive_catch',
		        	'DiveSave': '$dive_save,',
		        	'DivingSave': '$diving_save',
		        	'EffectiveClearances': '$effective_clearance',
		        	'AvgEffectiveClearances': {'$multiply': 
		        		[{'$divide': [{'$add': ['$effective_clearance', '$effective_head_clearance']}, '$total_clearance']}, '$appearances']},
		        	'EffectiveHeadClearance': '$effective_head_clearance',
		        	'GkSmother': '$gk_smother',
		        	'AvgGoalsConcededInBox': {'$multiply': 
		        		[{'$divide': ['$goals_conceded_ibox', '$goals_conceded']}, '$appearances']},
		        	'AvgGoalsConcededOutBox': {'$multiply': 
		        		[{'$divide': ['$goals_conceded_obox', '$goals_conceded']}, '$appearances']},
		        	'AvgGoodHighClaim': {'$multiply': 
		        		[{'$divide': ['$good_high_claim', '$total_high_claim']}, '$appearances']},
		        	'AvgKeeperPickUp': {'$divide': ['$keeper_pick_up', '$appearances']},
		        	'AvgLongPassOwnToOpp': {'$divide': ['$long_pass_own_to_opp', '$appearances']},
		        	'AvgLongPassOwnToOppSuccess': {'$divide': [{'$divide': ['$long_pass_own_to_opp_success', '$long_pass_own_to_opp']}, '$appearances']},
		        	'AvgLostCorners': {'$divide': ['$lost_corners', '$appearances']},
		        	'AvgOpenPlayPass': {'$divide': ['$open_play_pass', '$appearances']},
		        	'AvgPenGoalsConceded': {'$divide': ['$pen_goals_conceded', '$appearances']},
		        	'AvgPenaltyFaced': {'$divide': ['$penalty_faced', '$appearances']},
		        	'AvgPenaltySave': {'$divide': ['$penalty_save', '$penalty_faced']},
		        	'AvgPossLostAll': {'$divide': ['$poss_lost_all', '$appearances']},
		        	'AvgPossLostCtrl': {'$divide': ['$poss_lost_ctrl', '$appearances']},
		        	'AvgPossWonDef3rd': {'$divide': ['$poss_won_def_3rd', '$appearances']},
		        	'AvgSavedInbox': {'$multiply': [
		        			{'$divide': ['$saved_ibox', '$saves']}, '$appearances']},
		        	'AvgSavedOutbox': {'$multiply': [
		        			{'$divide': ['$saved_obox', '$saves']}, '$appearances']},
		        	'TotalSaves': '$saves',
		        	'AvgSaves': {'$divide': ['$saves', '$appearances']},
		        	'AvgStandCatch': {'$divide': ['$stand_catch', '$appearances']},
		        	'AvgStandSave': {'$divide': ['$stand_save', '$saves']},
		        	'AvgTouches': {'$divide': ['$touches', '$appearances']},
		        	'Id': '$p_id',
		        	'Team': '$team_shortName',
		        	'TeamId': '$team_id',
		        	'Position': '$position'

		        },
		    },

		]
		db = PlayersDB(self.league, self.season)
		return db.collection.aggregate(pipeline)
		

if __name__ == '__main__':
	data = list(DBCleaning('EN_PR', '2019').goalkeeper_collection())
	with open('../test_data/gk.json', 'w') as f:
		json.dump(data, f)


