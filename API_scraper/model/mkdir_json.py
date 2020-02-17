#Function to create the json folder to hold all json files
#mkdir_json

#Function to create subfolder depending on depth in json direktory
#Example
# json  
#   |--premier_league
#   |        |----compseason
#   |                 |-------standings
#   |                 |            |-----team_standing.json xTotal teams
#   |                 |
#   |                 |----fixture_stats.json
#   |                 |----player_stats.json           
#   |                 |----team_stats.json
#   |
#   |--competitions_id.json
#   |--compseason_id.json
#   |--fixtures_id.json
#   |--team_id.json

import os

def mkdir_json(*args):
	"""Creates folder in the same level as the working directory folder

		Args:

			*Args: path to folder that is to be created
	"""
	working_dir = os.path.dirname(__file__) #Get's the current working directory

	target_dir = os.path.join(working_dir, *args)
	try: 
		if os.path.exists(target_dir) == True:
			print(target_dir, 'exists')
		else:
			os.mkdir(os.path.join(working_dir, *args))
			print(os.path.join(working_dir, *args), 'succesfully created')
	except OSError as e:
		print(folder,'coult not be created', e)
	
if __name__ == '__main__':
	pass
